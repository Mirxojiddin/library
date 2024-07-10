document.addEventListener('DOMContentLoaded', function() {
    const provinceField = document.getElementById('id_province');
    const districtField = document.getElementById('id_district');
    const cityField = document.getElementById('id_city');

    provinceField.addEventListener('change', function() {
        const provinceId = provinceField.value;
        const url = '/ajax/load-districts/';
        fetch(url + '?province_id=' + provinceId)
            .then(response => response.json())
            .then(data => {
                districtField.innerHTML = '<option value="">_______</option>';
                data.forEach(district => {
                    const option = document.createElement('option');
                    option.value = district.id;
                    option.textContent = district.name;
                    districtField.appendChild(option);
                });
                districtField.dispatchEvent(new Event('change'));
            });
    });

    districtField.addEventListener('change', function() {
        const districtId = districtField.value;
        const url = '/ajax/load-cities/';
        fetch(url + '?district_id=' + districtId)
            .then(response => response.json())
            .then(data => {
                cityField.innerHTML = '<option value="">_______</option>';
                data.forEach(city => {
                    const option = document.createElement('option');
                    option.value = city.id;
                    option.textContent = city.name;
                    cityField.appendChild(option);
                });
            });
    });
});