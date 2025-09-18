function toggleCalibration() {
  document.getElementById('calibration').classList.toggle('hidden');
}

function handleFiles(files) {
  if (!files.length) return;
  const file = files[0];
  previewFile(file);
  uploadFile(file);
}

function previewFile(file) {
  const reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onloadend = function() {
    const img = document.createElement('img');
    img.src = reader.result;
    img.classList.add('preview-img');
    const preview = document.getElementById('preview');
    preview.innerHTML = '';
    preview.appendChild(img);
  };
}

function uploadFile(file) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('cal_low_x', document.getElementById('cal_low_x').value);
  formData.append('cal_low_y', document.getElementById('cal_low_y').value);
  formData.append('cal_high_x', document.getElementById('cal_high_x').value);
  formData.append('cal_high_y', document.getElementById('cal_high_y').value);

  const resultDiv = document.getElementById('result');
  resultDiv.innerHTML = '<p>กำลังวิเคราะห์...</p>';

  fetch('/analyze', { method: 'POST', body: formData })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        resultDiv.innerHTML = '<p class="error">' + data.error + '</p>';
      } else {
        resultDiv.innerHTML = '<h2>ผลการวิเคราะห์</h2>' +
          '<p><b>Luminance:</b> ' + data.luminance.toFixed(2) + '</p>' +
          '<p><b>ความเข้มข้น (mg/L):</b> ' + data.mg_per_l.toFixed(2) + '</p>';
      }
    })
    .catch(() => {
      resultDiv.innerHTML = '<p class="error">การอัปโหลดล้มเหลว</p>';
    });
}
