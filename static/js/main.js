const form = document.getElementById('predictForm');
const resultDiv = document.getElementById('predictResult');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const fileInput = form.querySelector('input[name="file"]');
  if (!fileInput.files.length) {
    alert('กรุณาเลือกไฟล์รูปภาพ');
    return;
  }

  const formData = new FormData();
  formData.append('file', fileInput.files[0]);

  resultDiv.textContent = 'กำลังประมวลผล...';

  try {
    const response = await fetch('/predict', {
      method: 'POST',
      body: formData
    });
    const data = await response.json();
    if (data.success) {
      resultDiv.textContent = `ความเข้มข้น: ${data.concentration.toFixed(2)} mg/L`;
    } else {
      resultDiv.textContent = `เกิดข้อผิดพลาด: ${data.error}`;
    }
  } catch (err) {
    resultDiv.textContent = 'เกิดข้อผิดพลาดในการเชื่อมต่อ';
  }
});
