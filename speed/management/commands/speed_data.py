from django.core.management.base import BaseCommand, CommandError

from speed import models


class Command(BaseCommand):
    help = "Dummy data"

    def handle(self, *args, **options):
        for name in ("Opel", "Ford", "Jeep", "Ferrari", "Mazda",
            "Mercedes", "Audi", "BMW :(", "Toyota", "Porsche",
            "Volvo", "Kia", "Volkswagen", "Hyundai"):
            models.Car.objects.create(title=name)

        for name_top in ("A", "B", "C", "D", "E"):
            obj_top = models.Container.objects.create(title="Top %s" % name_top)
            obj_top.target = models.Car.objects.all().order_by("?")[0]
            obj_top.save()
            for name_sub in range(20):
                obj_sub = models.Container.objects.create(
                    title="Sub %s" % name_sub,
                    parent=obj_top
                )
                obj_sub.target = models.Car.objects.all().order_by("?")[0]
                obj_sub.save()
