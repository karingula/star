import coreapi


flight_document = coreapi.Document(
    title = 'Flight Search API',
    url = 'https://api.flight.com'
    content = {
        'search': coreapi.Link(
            url='/search',
            action='GET',
            method='get_flight_details',
            fields=[
                coreapi.Field(
                    name='from',
                    required=True,
                    location='query',
                    description="City name or Airport code"
                ),
                coreapi.Field(
                    name='to',
                    required=True,
                    location='query',
                    description="City name or Airport code"
                ),
                coreapi.Field(
                    name='schedule',
                    required=True,
                    location='query',
                    description="Flight date"
                )
            ]
        )
    }
)


title = 'Flight Search API',
url = 'https://api.example.org/',
content = {
    'search': coreapi.Link(
        url='/search/',
        action='get',
        fields=[
            coreapi.Field(
                name='from',
                required=True,
                location='query',
                description='City name or airport code.'
            ),
            coreapi.Field(
                name='to',
                required=True,
                location='query',
                description='City name or airport code.'
            ),
            coreapi.Field(
                name='date',
                required=True,
                location='query',
                description='Flight date in "YYYY-MM-DD" format.'
            )
        ],
        description='Return flight availability and prices.'
}
