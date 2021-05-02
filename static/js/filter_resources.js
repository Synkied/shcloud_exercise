// Filtering resources by resource type and location

let resource_choice = document.getElementById('id_resource')
let resources = document.getElementById('id_resource').options
let defaultOption = resources[0].outerHTML // default option

async function getResources(filters) {
  try {
    let api_filters = ''
    counter = 0
    for (const [key, value] of Object.entries(filters)) {
      if (counter == 0) {
        api_filters += `?${key}=${value}`
      } else {
        api_filters += `&${key}=${value}`
      }
      counter += 1
    }
    let response = await axios.get(`/api/resource${api_filters}`)
    let results = response.data.results
    return results
  } catch (err) {
    console.error(err)
  }
}

let location_choice = document.getElementById("id_location")
let resource_type_choice = document.getElementById("id_resource_type")

let filters = {
  'location': location_choice.value,
  'resource_type': resource_type_choice.value
}

location_choice.addEventListener("change", async function () {
  filters['location'] = location_choice.value
  resources = await getResources(filters)
  buildOptions(resources)
})

resource_type_choice.addEventListener("change", async function () {
  filters['resource_type'] = resource_type_choice.value
  resources = await getResources(filters)
  buildOptions(resources)
});

function buildOptions (resources) {
  // dynamically build new options after filtering
  let newOptions = [
    defaultOption
  ]
  for (var i = resources.length - 1; i >= 0; i--) {
    let newOptionsHtml = `<option value=${resources[i].pk}>${resources[i].long_name}</option>`
    newOptions.push(newOptionsHtml)
  }
  resource_choice.innerHTML = newOptions;
}
