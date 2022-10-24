function getLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(showPosition);
    } else {
      alert("Geolocation is not supported by this browser.");
    }
  }
  function showPosition(position) {
    var lat = position.coords.latitude;
    var lng = position.coords.longitude;
    map.setCenter(new google.maps.LatLng(lat, lng));
  }