from collections import OrderedDict

from django.contrib.contenttypes.models import ContentType
from django.views.generic import TemplateView

from speed import models


class Wrapper(object):

    def __init__(self, context, target):
        self._context = context
        self._target = target

    def __getattr__(self, name):
        try:
            return super(Wrapper, self).__getattr__(name)
        except AttributeError:
            return getattr(self._context, name)

    @property
    def target(self):
        return self._target


class TreeView1(TemplateView):
    """Unoptimized"""

    def get_context_data(self, **kwargs):
        di = super(TreeView1, self).get_context_data(**kwargs)
        di["object_list"] = models.Container.objects.filter(parent=None)
        return di


class TreeView2(TemplateView):
    """Hierarchy in a single query"""

    def get_context_data(self, **kwargs):
        di = super(TreeView2, self).get_context_data(**kwargs)

        # One query
        containers = models.Container.objects.all().select_related("parent")

        # Tree
        tree = OrderedDict()
        for container in containers:
            parent = container.parent
            if parent is not None:
                if parent not in tree:
                    tree[parent] = []
                tree[parent].append(container)

        di["tree"] = tree
        return di


class TreeView3(TemplateView):
    """Hierarchy in a single query, generic foreigns keys optimized"""

    def get_context_data(self, **kwargs):
        di = super(TreeView3, self).get_context_data(**kwargs)

        # One query
        containers = models.Container.objects.all().select_related("parent")

        # Key is content type id, value is target id
        map_ct_targets = {}

        # Key one is content type id, key two is target id, value is a list of
        # containers.
        map_two_deep = {}

        # Populate the dictionaries
        for container in containers:
            ct_id = container.target_content_type_id
            target_id = container.target_object_id

            # map_ct_targets
            if ct_id not in map_ct_targets:
                map_ct_targets[ct_id] = []
            map_ct_targets[ct_id].append(target_id)

            # map_two_deep
            if ct_id not in map_two_deep:
                map_two_deep[ct_id] = {}
            if target_id not in map_two_deep[ct_id]:
                map_two_deep[ct_id][target_id] = []
            map_two_deep[ct_id][target_id].append(container)

        # Pre-lookup the content types
        content_types = {}
        for ct in ContentType.objects.filter(id__in=map_ct_targets.keys()):
            content_types[ct.id] = ct

        # Set the target objects on the containers
        for ct_id, ids in map_ct_targets.items():
            for obj in content_types[ct_id].model_class().objects.filter(id__in=ids):
                for container in map_two_deep[ct_id][obj.id]:
                    # Naughty! Inventing my own attribute.
                    container.mytarget = obj

        # Tree
        tree = OrderedDict()
        for container in containers:
            parent = container.parent
            if parent is not None:
                if parent not in tree:
                    tree[parent] = []
                tree[parent].append(container)

        di["tree"] = tree
        return di


class TreeView4(TemplateView):
    """Optimized and strictly correct"""

    def get_context_data(self, **kwargs):
        di = super(TreeView4, self).get_context_data(**kwargs)

        # One query
        containers = models.Container.objects.all().select_related("parent")

        # Key is content type id, value is target id
        map_ct_targets = {}

        # Key one is content type id, key two is target id, value is a list of
        # containers.
        map_two_deep = {}

        # Populate the dictionaries
        for container in containers:
            ct_id = container.target_content_type_id
            target_id = container.target_object_id

            # map_ct_targets
            if ct_id not in map_ct_targets:
                map_ct_targets[ct_id] = []
            map_ct_targets[ct_id].append(target_id)

            # map_two_deep
            if ct_id not in map_two_deep:
                map_two_deep[ct_id] = {}
            if target_id not in map_two_deep[ct_id]:
                map_two_deep[ct_id][target_id] = []
            map_two_deep[ct_id][target_id].append(container)

        # Pre-lookup the content types
        content_types = {}
        for ct in ContentType.objects.filter(id__in=map_ct_targets.keys()):
            content_types[ct.id] = ct

        # Map the target objects on the containers
        wrapped_containers = {}
        for ct_id, ids in map_ct_targets.items():
            for obj in content_types[ct_id].model_class().objects.filter(id__in=ids):
                for container in map_two_deep[ct_id][obj.id]:
                    wrapped_containers[container.id] = Wrapper(container, target=obj)

        # Tree
        tree = OrderedDict()
        for container in containers:
            container = wrapped_containers[container.id]
            parent = container.parent
            if parent is not None:
                parent = wrapped_containers[parent.id]
                #Wrapped(parent, container_targets[parent.id]
                if parent not in tree:
                    tree[parent] = []
                tree[parent].append(container)

        di["tree"] = tree
        return di
