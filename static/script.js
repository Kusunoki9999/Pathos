function dmsToDecimal(dmsArray) {
    const degrees = dmsArray[0];
    const minutes = dmsArray[1];
    const seconds = dmsArray[2];
    return degrees + (minutes / 60) + (seconds / 3600);
}

async function initMap() {
    const response = await fetch('/user-post-details');
    const postDetails = await response.json();

    const map = new google.map.Map(document.getElementById("map-container"),{
        center : {lat: 38.151550, lng: 137.410380},
        zoom: 4,
    });

    postDetail.forEach(post => {
        const lat = dmsToDecimal(post.gps.GPSLatitude);
        const lng = dmsToDecimal(post.gps.GPSLongitude);

        const marker = new google.maps.Marker({
            position: {lat, lng},
            map,
            title: post.title
        });
    });
    
    const infoWindow = new google.maps.InfoWindow({
        content:  `<div><h3>${post.title}</h3><p>${post.caption}</p></div>`,
    });
}

async function loadGoogleMapsAPI() {
    try {
        const response = await fetch('/api-key');
        const data = await response.json();
        console.log(data)
        const api_key = data.api_key;

        const script = document.createElement('script');
        script.src = `https://maps.googleapis.com/maps/api/js?key=${api_key}&callback=initMap&libraries=marker&v=beta&solution_channel=GMP_CCS_infowindows_v2`;
        script.defer = true;
        document.head.appendChild(script);
    } catch (error) {
        console.error('APIキー取得ならず', error);
    }
}

// 読み込み時にAPIロード
window.onload = loadGoogleMapsAPI;
