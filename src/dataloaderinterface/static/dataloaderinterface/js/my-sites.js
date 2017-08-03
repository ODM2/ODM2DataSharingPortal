/**
 * Created by Juan on 1/24/2017.
 */

function initMap() {
    const DEFAULT_ZOOM = 5;
    const DEFAULT_LATITUDE = 37.0902;
    const DEFAULT_LONGITUDE = -95.7129;
    const DEFAULT_POSITION = { lat: DEFAULT_LATITUDE, lng: DEFAULT_LONGITUDE };
    var ZOOM_LEVEL = sessionStorage && parseInt(sessionStorage.getItem('MY_CURRENT_ZOOM')) || DEFAULT_ZOOM;
    var temp = sessionStorage.getItem('MY_CURRENT_CENTER');

    if(sessionStorage.getItem('MY_CURRENT_CENTER')){
        var CUR_CENTER = getLatLngFromString(temp);
        var MAP_CENTER =  CUR_CENTER;
    }
    else{
        var MAP_CENTER = DEFAULT_POSITION;
    }

    console.log(MAP_CENTER);

    var markerData = JSON.parse(document.getElementById('sites-data').innerHTML);

    var map = new google.maps.Map(document.getElementById('map'), {
        center: MAP_CENTER,
        zoom: ZOOM_LEVEL,
        disableDefaultUI: true,
        zoomControl: true,
        zoomControlOptions: {
            position: google.maps.ControlPosition.LEFT_BOTTOM
        },
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        scaleControl: true
    });

    map.addListener('zoom_changed', function(){
        var CURRENT_ZOOM = map.getZoom();

        sessionStorage.setItem('MY_CURRENT_ZOOM', CURRENT_ZOOM);
    });

    map.addListener('center_changed', function(){
        var CURRENT_CENTER = map.getCenter();

        sessionStorage.setItem('MY_CURRENT_CENTER', CURRENT_CENTER);
    });

    var bounds = new google.maps.LatLngBounds();
    var infoWindow = new google.maps.InfoWindow({
        content: ''
    });

    markerData.forEach(function(site) {
        var marker = new google.maps.Marker({
            position: { lat: site.latitude, lng: site.longitude },
            map: map
        });

        bounds.extend(marker.getPosition());

        marker.addListener('click', function() {
            var infoContent = createInfoWindowContent(site);
            infoWindow.setContent(infoContent);
            infoWindow.open(marker.get('map'), marker);
        });

        $('.site[data-site=' + site.id + '] .view-on-map').on('click', { 'site-data': site, 'marker': marker, 'info-window': infoWindow }, function(event) {
            var data = event.data['site-data'];
            map.setCenter({ lat: data.latitude, lng: data.longitude });
            map.setZoom(16);

            var infoContent = createInfoWindowContent(data);
            event.data['info-window'].setContent(infoContent);
            event.data['info-window'].open(marker.get('map'), marker);

            $('html, body').animate({
                scrollTop: 0
            }, 150);
        });
    });

    if (!sessionStorage.getItem('MY_CURRENT_CENTER')){
        map.fitBounds(bounds);
    }
}

function createInfoWindowContent(siteInfo) {
    var contentElement = $('<div></div>').append($('#site-marker-content').html());
    var fields = contentElement.find('.site-field');
    fields.each(function(index, element) {
        var field = $(element).data('field');
        $(element).find('.site-data').text(siteInfo[field]);
    });
    contentElement.find('.site-link a').attr('href', siteInfo.detail_link);

    return $('<div></div>').append(contentElement.html()).html();
}

// Makes all site cards have the same height.
function fixViewPort() {
    var cards = $('.site-card');

    var maxHeight = 0;
    for (var i = 0; i < cards.length; i++) {
        maxHeight = Math.max($(cards[i]).height(), maxHeight);
    }

    // set to new max height
    for (var i = 0; i < cards.length; i++) {
        $(cards[i]).height(maxHeight);
    }
}

$(document).ready(function () {
    $('nav .menu-sites-list').addClass('active');

    // Executes when page loads
    fixViewPort();

    // Executes each time window size changes
    $(window).resize(
        ResponsiveBootstrapToolkit.changed(function () {
            $('.site-card').height("initial");   // Reset height
            fixViewPort();
        })
    );
});

function getLatLngFromString(location) {
    var latlang = location.replace(/[()]/g,'');
    var latlng = latlang.split(',');
    var locate = new google.maps.LatLng(parseFloat(latlng[0]) , parseFloat(latlng[1]));
    return locate;
}