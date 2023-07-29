from .models import Stats, Visits

def stats_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Change here!! this code will be executed for all requests

        # Code to be executed for each request before
        # the view (and later middleware) are called.
        
        
        if not Stats.objects.filter(id=1):
            Stats.objects.create(id=1,name='occurence',value=0).save()
        if not Visits.objects.filter(id=1):
            Visits.objects.create(id=1,number_of_visits=0).save()
            
        obj=Stats.objects.get(id=1)
        obj.value+=1
        obj.save()
        from django.utils import timezone
        now=timezone.now().date()
        visits=Visits.objects.filter(date_time=now)
        if (not visits):
            visits=Visits.objects.create(date_time=now,number_of_visits=1)
        else:
            visits=visits[0]
        visits.number_of_visits+=1
        visits.save()

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware