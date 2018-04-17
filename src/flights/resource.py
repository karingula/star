from apistar import http
from typing import List
from ...orm.models import Flight

class FlightResource():
    """This is a Flight Resource
    """
    def get_flight_details(request: http.Request):
        print(request.method)
        data = [FlightComponent(instance)
                for instance in session.query(Flight).all()]

        return render_template('flights.html', data=data)

    def add_flight(data:http.RequestData):
        
        #---------Getting the data from form and constructing the Dataframe
        flight_data = data.to_dict(flat=False)
        # The uploadedfile is of type list of FileStorage
        print(type(flight_data['uploadedfile']))
        #save the file object as dst
        flight_data['uploadedfile'][0].save('dst')
        # read the csv file object to dataframe
        df= pd.read_csv('dst')

        return "Sleep with Fishes!"
