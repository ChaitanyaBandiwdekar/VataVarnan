import { Streamlit } from "./streamlit"
import * as L from "leaflet"
import "leaflet/dist/leaflet.css"
import { useEffect, useState } from "react"
import { getPositionOfLineAndCharacter } from "typescript"

const map = document.createElement("div")
map.style.height = "600px"
map.setAttribute("id", "mapid")
document.body.appendChild(map);
let coordinates = [10, 10];
// async function getPosition(){
//   let latitude = 10;
//   let longitude = 10;

//   navigator.geolocation.getCurrentPosition((position) => { 
//     console.log("Got position", position.coords);
//     latitude = position.coords.latitude
//     longitude = position.coords.longitude
//   }); 
//   return [latitude, longitude]
// }

// let coordinates = await getPosition();
// console.log(coordinates);

const mymap = L.map("mapid").setView([19.074132, 72.899554], 13)

L.tileLayer(
  "https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1Ijoib3hpZGFuZTc3NyIsImEiOiJjbDFzZW9zZXkyMzFsM2NvMjdpMGpoZG4yIn0.3wG5QKi4FC7I8dAouJAR2Q",
  {
    attribution:
      'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: "mapbox/streets-v11",
    tileSize: 512,
    zoomOffset: -1,
    accessToken: "use.your.mapbox.token",
  }
).addTo(mymap)

function onMapClick(e: any) {
  L.popup()
    .setLatLng(e.latlng)
    .setContent("Location selected: " + e.latlng.toString())
    .openOn(mymap)
  Streamlit.setComponentValue(e.latlng)
  Streamlit.setFrameHeight()
}
mymap.on("click", onMapClick)

function onRender(event: Event): void {
  Streamlit.setFrameHeight()
}
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)

Streamlit.setComponentReady()
Streamlit.setFrameHeight()
