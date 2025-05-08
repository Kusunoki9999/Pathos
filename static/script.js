function dmsToDecimal(dmsArray) {
    const degrees = dmsArray[0];
    const minutes = dmsArray[1];
    const seconds = dmsArray[2];
    return degrees + (minutes / 60) + (seconds / 3600);
}

async function initMap() {
    const response = await fetch('/user-post-details');
    const postDetails = await response.json();

    const map = new google.maps.Map(document.getElementById("map-container"),{
        center : {lat: 38.151550, lng: 137.410380},
        zoom: 4,
    });

    postDetails.forEach(post => {
        if (!post.gps || !post.gps.GPSLatitude || !post.gps.GPSLongitude) {
            console.error("GPS data is missing for post:", post);
            return; // データがない場合スキップ
        }
        
        const lat = dmsToDecimal(post.gps.GPSLatitude);
        const lng = dmsToDecimal(post.gps.GPSLongitude);

        const marker = new google.maps.Marker({
            position: {lat, lng},
            map,
            title: post.title
        });

        const infoWindow = new google.maps.InfoWindow({
            content:  `<div>
                            <h3>${post.title}</h3>
                            <p>${post.caption}</p>
                            <img src="${post.image_path}" style="max-width: 200px; height: auto;">
                        </div>`,
        });

        marker.addListener("click",() => {
            infoWindow.open(map, marker);
        })
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

async function fetchCurrentUser() {
    console.log("✅ fetchCurrentUser() が呼ばれました");

    const token = localStorage.getItem("access_token");
    console.log("🔑 取得したトークン:", token);

    if (!token) {
        console.log("🚫 トークンが見つかりません。未ログインと判定します。");
        document.getElementById("current-user").innerText = "未ログイン";
        return;
    }

    try {
        const res = await fetch("/auth/users/me", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        console.log("📡 サーバーからのレスポンス:", res.status);

        if (res.ok) {
            const user = await res.json();
            console.log("👤 取得したユーザー情報:", user);
            document.getElementById("current-user").innerText = user.username;
        } else {
            console.warn("ユーザー情報の取得に失敗しました:", await res.text());
            document.getElementById("current-user").innerText = "未ログイン";
        }
    } catch (error) {
        console.error("fetchCurrentUser中の例外:", error);
        document.getElementById("current-user").innerText = "未ログイン";
    }
}


document.addEventListener("DOMContentLoaded", async () => {
    console.log("DOMContentLoaded 発火");
    await loadGoogleMapsAPI();
    await fetchCurrentUser();
});


/*
正しく動作していないためDOMContentLoadイベントに修正
window.onload = async () => {
    await loadGoogleMapsAPI();
    await fetchCurrentUser(); // 追加
};
*/
