window.onload = function () {
    $('#down').on('click',function () {
		$("html").scrollTop(0);
		console.log("Clicked!");
		 $('html, body').animate({
        scrollTop: $("#wrapper").offset().top
    }, 1000);
	});


    d3.text("./static/motion_info.csv", function(data) {
        var parsedCSV = d3.csv.parseRows(data);

        var container = d3.select("#motion-info")
            .append("table")

            .selectAll("tr")
                .data(parsedCSV).enter()
                .append("tr")

            .selectAll("td")
                .data(function(d) { return d; }).enter()
                .append("td")
                .text(function(d) { return d; });
        
    });

    function getColor(vote) {
        ret_val = ''

        if (vote === 'Yes-Yes') {
            ret_val = '#1a9641'
        } else if (vote == 'Yes-Absent') {
            ret_val = '#a6d96a'
        } else if (vote == 'Yes-No') {
            ret_val = '#ffff0f'
        } else if (vote == 'No-Absent') {
            ret_val = '#fdae61'
        } else if (vote == 'No-No') {
            ret_val = '#d7191c'
        } else {
            ret_val = 'white'
        }
        return ret_val
    }

    function style(feature) {
        return {
            fillColor: getColor(feature.properties.final_vote),
            weight: 2,
            opacity: 1,
            color: 'white',
            dashArray: '3',
            fillOpacity: 0.8
        };
    }







    function create_icons(ward_num) {
        var myIcon = L.divIcon({})
    }

    function on_each_feature(feature, layer) {
        layer.bindPopup('<h4 style="font-weight: bold">Ward ' + feature.properties.ward_num + '</h4><img src="' + feature.properties.councillor_x_img + '" alt="Snow" style="width:100%"> <p><span style="font-weight:bold">' + feature.properties.councillor_x_full_name + ' voted ' + feature.properties.vote_x + '</span></br>' + feature.properties.councillor_x_email + '<br>' + feature.properties.councillor_x_phone + '</p><br><img src="' + feature.properties.councillor_y_img + '" alt="Snow" style="width:100%"><p><span style="font-weight:bold">' + feature.properties.councillor_y_full_name + ' voted ' + feature.properties.vote_y + '</span></br>' + feature.properties.councillor_y_email + '<br>' + feature.properties.councillor_y_phone + '</p>');
        //layer.bindTooltip('<h1 style="font-size: 25px; color: rgba(0, 0, 0, 0.5);"> ' + feature.properties.ward_num + '</h1>', {permanent: true});


        // var my_icon = L.divIcon('<h1 style="font-size: 50px; color: rgba(0, 0, 0, 0.5);"> ' + feature.properties.ward_num + '</h1>')




        // L.marker([lat, lon], {icon: my_icon})
    }

    var basemap = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}', {
        attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ',
        maxZoom: 16
    });

    $.getJSON("/static/result.geojson", function(data) {

    


        var geojson = L.geoJson(data, {
            style: style,
            onEachFeature: on_each_feature
        }); 



        var map = L.map('my-map')
        .fitBounds(geojson.getBounds());
    //    .setView([0.0,-10.0], 2);

        var startPos;
        navigator.geolocation.getCurrentPosition(function(position) {
            startPos = position;
            var lat = startPos.coords.latitude;
            var lon = startPos.coords.longitude;
            
            var marker = L.marker([lat, lon]).addTo(map);
        });

        /*Legend specific*/
        var legend = L.control({ position: "bottomleft" });

        legend.onAdd = function(map) {
        var div = L.DomUtil.create("div", "legend");
        div.innerHTML += "<h4>LEGEND</h4>";
        div.innerHTML += '<i style="background: #1a9641"></i><span>Yes-Yes</span><br>';
        div.innerHTML += '<i style="background: #a6d96a"></i><span>Yes-Absent</span><br>';
        div.innerHTML += '<i style="background: #ffffbf"></i><span>Yes-No</span><br>';
        div.innerHTML += '<i style="background: #fdae61"></i><span>No-Absent</span><br>';
        div.innerHTML += '<i style="background: #d7191c"></i><span>No-No</span><br>';
        div.innerHTML += '<i style="background: black"></i><span>Absent-Absent</span><br>';

        
        
        

        return div;
        };

      
        // $.getJSON('https://opendata.arcgis.com/datasets/fdbfe289276a46e2b9ac8195b45c9a22_0.geojson', function(data) {
        //     L.geoJSON(data).addTo(map);
        // });


        // final_markers()

        L.control.scale({
            metric: true,
            imperial: false
        }).addTo(map)

        legend.addTo(map);
        basemap.addTo(map);
        geojson.addTo(map);
  });

};