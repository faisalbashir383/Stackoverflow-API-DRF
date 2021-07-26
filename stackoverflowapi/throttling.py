from rest_framework.throttling import UserRateThrottle

class FaisalRateThrottle(UserRateThrottle):
    scope='faisal'