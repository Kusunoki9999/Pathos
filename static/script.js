function dmsToDecimal(dmsArray) {
    const degrees = dmsArray[0];
    const minutes = dmsArray[1];
    const seconds = dmsArray[2];
    return degrees + (minutes / 60) + (seconds / 3600);
}

async function initMap() {

    const response = await fetch('/user-post-details');
    const postDetails = await response.json();
    
    const contentString = `
    <div>
        <h1>Sapporo</h1>
        <div>
            <p>
                Sapporo center park
            </p>
            <img src="https://www.visit-hokkaido.jp/lsc/upfile/spot/0001/0004/10004_1_l.jpg" width="300" height="200">
        </div>
    </div>`;
    const infoWindow = new google.maps.InfoWindow({
        content: contentString,
        ariaLabel: "sapporo",
    });

    const marker = document.querySelector('gmp-advanced-marker');
    marker.addEventListener('gmp-click', () => {
        infoWindow.open({ anchor: marker });
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
