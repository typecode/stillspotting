if(!tc){ var tc = {}; }

if(!tc.gmap){ tc.gmap = {}; }

tc.gmap.tc_styles = {
  base:[
    {
      featureType: "landscape",
      elementType: "all",
      stylers: [
        { visibility: "on" }
      ]
    },{
      featureType: "poi",
      elementType: "all",
      stylers: [
        { visibility: "off" }
      ]
    },{
      featureType: "road",
      elementType: "all",
      stylers: [
        { visibility: "off" }
      ]
    },{
      featureType: "transit",
      elementType: "all",
      stylers: [
        { visibility: "off" }
      ]
    },{
      featureType: "administrative",
      elementType: "all",
      stylers: [
        { visibility: "off" }
      ]
    },{
      featureType: "poi",
      elementType: "all",
      stylers: [
        { visibility: "off" }
      ]
    },{
      featureType: "poi.park",
      elementType: "all",
      stylers: [
        { visibility: "on" }
      ]
    },{
      featureType: "all",
      elementType: "labels",
      stylers: [
        { visibility: "off" }
      ]
    },{
      featureType: "all",
      elementType: "all",
      stylers: [

      ]
    }
  ]
}

tc.gmap.styledMapTypes = {
  base: new google.maps.StyledMapType(tc.gmap.tc_styles.base, {
    name:'TYPE/CODE',
    minZoom:4
  })
}