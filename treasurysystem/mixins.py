from django.db.models import Q
from functools import reduce
import operator

class SearchableMixin:
    @classmethod
    def search(cls, query):
        if not hasattr(cls, 'search_fields'):
            return cls.objects.none()
            
        if not query:
            return cls.objects.all()
            
        search_terms = query.split()
        
        # Build Q objects for each search term and each field
        q_objects = [
            Q(**{f"{field}__icontains": term})
            for field in cls.search_fields
            for term in search_terms
        ]
        
        # Combine Q objects with OR operator
        return cls.objects.filter(reduce(operator.or_, q_objects))
