import os
import sys
from urllib.parse import urlencode

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
for candidate in [
    os.path.join(BASE_DIR, ".venv-site-packages"),
    r"D:\mini-tour-kpp-deps",
]:
    if os.path.isdir(candidate) and candidate not in sys.path:
        sys.path.insert(0, candidate)

from flask import Flask, render_template
import folium
from folium.plugins import Fullscreen

app = Flask(__name__)

places = [
    {
        "id": 1,
        "name": "หอพักณัชชา 2",
        "description": "จุดเริ่มต้นของการเดินทางในจังหวัดกำแพงเพชร เพื่อเตรียมพลังก่อนลุยทริปธรรมชาติอย่างเต็มที่",
        "lat": 16.462563346635413,
        "lon": 99.51859916573929,
        "image": "https://images.unsplash.com/photo-1554995207-c18c203602cb?auto=format&fit=crop&q=80&w=800",
        "google_maps_url": "https://www.google.com/maps/dir/?api=1&destination=16.462563346635413,99.51859916573929",
    },
    {
        "id": 2,
        "name": "ชาใจ story",
        "description": "คาเฟ่เก๋ๆ ที่เหมาะกับการพักเครื่องและเติมพลังด้วยเครื่องดื่มและขนมอร่อยก่อนเดินทางต่อ",
        "lat": 16.458992414401433,
        "lon": 99.51780596758789,
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSK_1Fd2LPnA3yRX-bnLDPxHaaUmqNTGvwULyahEvomAw&s=10",
        "google_maps_url": "https://www.google.com/maps/dir/?api=1&destination=16.458992414401433,99.51780596758789",
    },
    {
        "id": 3,
        "name": "น้ำตกคลองลาน",
        "description": "น้ำตกขนาดใหญ่และงดงามที่มีชื่อเสียงแห่งหนึ่งของจังหวัดกำแพงเพชร อลังการและน่าทึ่งมาก",
        "lat": 16.129767275543724,
        "lon": 99.27458788107704,
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQs3hHDKoKbrzrGIrFK4nGU9KwQSxsa2FTj1x_TPn-Elw&s=10",
        "google_maps_url": "https://www.google.com/maps/dir/?api=1&destination=16.129767275543724,99.27458788107704",
    },
    {
        "id": 4,
        "name": "น้ำตกเต่าดำ",
        "description": "น้ำตกลับกลิ่นป่าที่ซ่อนตัวในธรรมชาติอันเงียบสงบ เหมาะกับการผ่อนคลายและถ่ายภาพ",
        "lat": 16.301919834377667,
        "lon": 99.11179431176345,
        "image": "https://s359.kapook.com/pagebuilder/9a4ac0a9-1c01-4a55-bdcc-4c24f4515e3a.jpg",
        "google_maps_url": "https://www.google.com/maps/dir/?api=1&destination=16.301919834377667,99.11179431176345",
    },
    {
        "id": 5,
        "name": "น้ำตกคลองน้ำไหล",
        "description": "น้ำตกที่มีชั้นน้ำเรียงกันสวยงาม เหมาะกับการสัมผัสธรรมชาติและพักผ่อนในวันเดียว",
        "lat": 16.193476973595192,
        "lon": 99.26067935593966,
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRVV5_FRjCAjPBVurI_cZM_B5yuoaQdZxevcm8OLyi7lA&s=10",
        "google_maps_url": "https://www.google.com/maps/dir/?api=1&destination=16.193476973595192,99.26067935593966",
    },
]


def build_google_maps_route_url(route_points):
    if not route_points:
        return "#"

    origin = route_points[0]
    destination = route_points[-1]
    waypoints = route_points[1:-1]

    params = {
        "api": 1,
        "origin": f"{origin['lat']},{origin['lon']}",
        "destination": f"{destination['lat']},{destination['lon']}",
    }
    if waypoints:
        params["waypoints"] = "|".join(f"{point['lat']},{point['lon']}" for point in waypoints)

    return "https://www.google.com/maps/dir/?" + urlencode(params)


@app.route("/")
def index():
    center_lat = sum(point["lat"] for point in places) / len(places)
    center_lon = sum(point["lon"] for point in places) / len(places)

    map_object = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=9,
        tiles="CartoDB dark_matter",
        control_scale=True,
    )
    Fullscreen(position="topright").add_to(map_object)

    coordinates = [[point["lat"], point["lon"]] for point in places]
    folium.PolyLine(
        locations=coordinates,
        color="#8b5cf6",
        weight=4,
        opacity=0.9,
        tooltip="เส้นทางทริป 1 วัน",
    ).add_to(map_object)

    for point in places:
        popup_html = f"""
        <div style="font-family: 'Prompt', sans-serif; min-width: 220px;">
            <h4 style="margin: 0 0 8px; color: #111827;">{point['name']}</h4>
            <img src="{point['image']}" style="width: 100%; height: 120px; object-fit: cover; border-radius: 10px; margin-bottom: 8px;">
            <p style="font-size: 12px; color: #4b5563; margin-bottom: 10px;">{point['description']}</p>
            <a href="{point['google_maps_url']}" target="_blank" style="display: block; background: linear-gradient(135deg, #8b5cf6, #38bdf8); color: white; text-align: center; padding: 8px; border-radius: 999px; text-decoration: none; font-size: 12px; font-weight: 700;">ข้อมูลเส้นทาง</a>
        </div>
        """

        folium.Marker(
            location=[point["lat"], point["lon"]],
            popup=folium.Popup(popup_html, max_width=320),
            tooltip=point["name"],
            icon=folium.Icon(color="purple", icon="info-sign"),
        ).add_to(map_object)

    explore_route_url = build_google_maps_route_url(places)
    map_html = map_object._repr_html_()

return render_template(
    "index.html",
    places=places,
    map_html=map_html,
    explore_route_url=explore_route_url,
)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5003)
