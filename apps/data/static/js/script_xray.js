function showUploadFields() {
    var uploadType = document.getElementById('upload_type').value;
    var cameraFields = document.getElementById('camera_fields');
    var dicomFields = document.getElementById('dicom_fields');

    if (uploadType === 'camera') {
        cameraFields.style.display = 'block';
        dicomFields.style.display = 'none';
    } else if (uploadType === 'dicom') {
        cameraFields.style.display = 'none';
        dicomFields.style.display = 'block';
    }
}

function showDicomFields() {
    var dicomType = document.getElementById('dicom_type').value;
    var combinedDicomField = document.getElementById('combined_dicom_field');
    var separateDicomFields = document.getElementById('separate_dicom_fields');

    if (dicomType === 'combined') {
        combinedDicomField.style.display = 'block';
        separateDicomFields.style.display = 'none';
    } else if (dicomType === 'separate') {
        combinedDicomField.style.display = 'none';
        separateDicomFields.style.display = 'block';
    }
}