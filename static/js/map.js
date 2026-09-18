(() => {
  const node = document.querySelector('#delivery-map');
  if (!node || !window.L) return;

  const latInput = document.querySelector('[name="delivery_latitude"]');
  const lngInput = document.querySelector('[name="delivery_longitude"]');
  const status = document.querySelector('#location-status');
  const methodInputs = document.querySelectorAll('[name="location_method"]');
  const panels = document.querySelectorAll('[data-location-panel]');
  // Restaurant location: Aleppo Al-Jadida Al-Shamali, north of Chicken House.
  const restaurantLocation = [36.20193, 37.09959];
  const map = L.map(node).setView(restaurantLocation, 14);
  let marker;

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '© OpenStreetMap' }).addTo(map);
  const setPoint = (latlng) => {
    if (marker) marker.setLatLng(latlng);
    else marker = L.marker(latlng, { draggable: true }).addTo(map).on('dragend', (event) => setPoint(event.target.getLatLng()));
    latInput.value = latlng.lat.toFixed(6);
    lngInput.value = latlng.lng.toFixed(6);
    status.textContent = 'تم تحديد موقع التوصيل. يمكنك سحب العلامة لتعديله.';
  };
  const setMethod = (method) => {
    panels.forEach((panel) => { panel.hidden = panel.dataset.locationPanel !== method; });
    if (method === 'map') setTimeout(() => map.invalidateSize(), 0);
  };

  const initialLat = parseFloat(node.dataset.lat), initialLng = parseFloat(node.dataset.lng);
  if (!Number.isNaN(initialLat) && !Number.isNaN(initialLng)) setPoint([initialLat, initialLng]);
  map.on('click', (event) => setPoint(event.latlng));
  methodInputs.forEach((input) => input.addEventListener('change', () => setMethod(input.value)));
  setMethod(document.querySelector('[name="location_method"]:checked')?.value || 'map');

  document.querySelector('#locate').addEventListener('click', () => {
    if (!navigator.geolocation) { status.textContent = 'متصفحك لا يدعم تحديد الموقع. اختره يدويًا من الخريطة.'; return; }
    status.textContent = 'جارٍ تحديد موقعك…';
    navigator.geolocation.getCurrentPosition((position) => {
      const point = [position.coords.latitude, position.coords.longitude];
      setPoint(point); map.setView(point, 16);
    }, () => { status.textContent = 'تعذر تحديد الموقع. اختره يدويًا من الخريطة أو اكتب العنوان.'; }, { enableHighAccuracy: true, timeout: 10000 });
  });
})();
