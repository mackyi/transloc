#==============================================================================#
#
# Module for the Trip class, which stores info about a user's suggested route.
#
#==============================================================================#

from api          import get_estimate
from walking      import walk_to, walk_from
from route_finder import get_directions 

class Trip:
    """
    Constructor

    Parameters;
        - trip: a (stop, route, stop) tuple of the suggested trip
    """
    def __init__(self, trip):
        # Get the route information
        self.i_stop = trip[0]
        self.route  = trip[1]
        self.f_stop = trip[2]

        self.update_estimates()

    """
    Update trip time.
    """
    def update_estimates(self):
        i_est = get_estimate(self.route['route_id'], self.i_stop['stop_id'])
        self.i_stop_est = i_est[0]['arrival_at']

        f_est = get_estimate(self.route['route_id'], self.f_stop['stop_id'])
        for est in f_est:
            if est['vehicle_id'] == i_est[0]['vehicle_id']:    # Ensure the shuttle is the same
                if est['arrival_at'] > i_est[0]['arrival_at']: # Ensure the arrival time is after departure
                    self.f_stop_est = est['arrival_at']
                    break

    """
    Get walking directions for the trip

    Parameters:
        - start: a (lat,lng) tuple
        - dest:  a (lat,lng) tuple
    """
    def walking_directions(self, start, dest):

        self.dir_to   = walk_to(start, self.i_stop)
        self.dir_from = walk_from(self.f_stop, dest) 

    """
    String

    Shows the start, the route, and the destination as a
    nicely formatted string.
    """
    def __str__(self):
        return "Start: " + self.i_stop['name'] + \
        " | Departure: " + self.i_stop_est[11:16] + '\n' + \
        "Route: "        + self.route['long_name'] + '\n' + \
        "Destination: "  + self.f_stop['name'] + \
        " | Arrival: "   + self.f_stop_est[11:16]

    """
    Set notifications.
    
    This would need to have something to do with getting within a radius of a stop.
    """
