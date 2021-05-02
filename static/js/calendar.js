// Reservations calendar handling
document.addEventListener('DOMContentLoaded', async function() {

  async function getResources() {
    try {
      let response = await axios.get('/api/resource')
      let results = response.data.results
      return results
    } catch (err) {
      console.error(err)
    }
  }

  async function getReservations() {
    try {
      let response = await axios.get('/api/reservation')
      let results = response.data.results
      return results
    } catch (err) {
      console.error(err)
    }
  }

  let resources = await getResources()
  let reservations = await getReservations()

  resources.map((resource, idx) => {
    resource.id = resource.pk
    resource.title = resource.label
  })

  reservations.map((reservation, idx) => {
    reservation.id = idx
    reservation.start = reservation.start_date
    reservation.end = reservation.end_date
  })

  var calendarEl = document.getElementById('calendar');
  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'resourceTimeGridTwoDay',
    timeZone: '{{ user.timezone }}',
    headerToolbar: {
      left: 'prev,next,today',
      center: 'title',
      right: 'resourceTimeGridDay,resourceTimeGridTwoDay'
    },
    views: {
      resourceTimeGridTwoDay: {
        type: 'resourceTimeGrid',
        duration: { days: 2 },
        buttonText: '2 days'
      }
    },
    nowIndicator: true,
    businessHours: {
      // days of week. an array of zero-based day of week integers (0=Sunday)
      daysOfWeek: [ 1, 2, 3, 4, 5 ], // Monday - Friday

      startTime: '08:00', // a start time (10am in this example)
      endTime: '20:00', // an end time (6pm in this example)
    },
    schedulerLicenseKey: 'CC-Attribution-NonCommercial-NoDerivatives',
    initialView: 'resourceTimeGridDay',
    resources: [...resources],
    events: [...reservations],
    height: 650,
    eventClick: function(info) {
      let reservation_pk = info.event.extendedProps.pk
      url = '{% url "reservation_detail" 888 %}'
      // cheat to get to corresponding url
      document.location.href = url.replace('888', reservation_pk);
    }
  });

  var events = calendar.getEvents();
  events.map(event => {
    event.setResources([event.extendedProps.resource])
  })
  calendar.render();
});

