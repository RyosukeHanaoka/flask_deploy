let rightHandImage = null;
let leftHandImage = null;
let currentHand = null;

const captureRightBtn = document.getElementById('captureRight');
const captureLeftBtn = document.getElementById('captureLeft');
const uploadPhotosBtn = document.getElementById('uploadPhotos');
const cameraView = document.getElementById('cameraView');
const previewView = document.getElementById('previewView');
const video = document.getElementById('video');
const takePhotoBtn = document.getElementById('takePhoto');
const preview = document.getElementById('preview');
const confirmPhotoBtn = document.getElementById('confirmPhoto');
const retakePhotoBtn = document.getElementById('retakePhoto');

captureRightBtn.addEventListener('click', () => startCamera('right'));
captureLeftBtn.addEventListener('click', () => startCamera('left'));
takePhotoBtn.addEventListener('click', takePhoto);
confirmPhotoBtn.addEventListener('click', confirmPhoto);
retakePhotoBtn.addEventListener('click', retakePhoto);
uploadPhotosBtn.addEventListener('click', uploadPhotos);

function startCamera(hand) {
    currentHand = hand;
    cameraView.style.display = 'block';
    captureRightBtn.style.display = 'none';
    captureLeftBtn.style.display = 'none';
    uploadPhotosBtn.style.display = 'none';

    navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
        .then(stream => {
            video.srcObject = stream;
        })
        .catch(error => {
            console.error('カメラへのアクセスに失敗しました:', error);
        });
}

function takePhoto() {
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    preview.src = canvas.toDataURL('image/jpeg');
    
    cameraView.style.display = 'none';
    previewView.style.display = 'block';

    // カメラストリームを停止
    video.srcObject.getTracks().forEach(track => track.stop());
}

function confirmPhoto() {
    if (currentHand === 'right') {
        rightHandImage = preview.src;
    } else {
        leftHandImage = preview.src;
    }

    previewView.style.display = 'none';
    captureRightBtn.style.display = 'inline-block';
    captureLeftBtn.style.display = 'inline-block';

    if (rightHandImage && leftHandImage) {
        uploadPhotosBtn.style.display = 'inline-block';
    }
}

function retakePhoto() {
    previewView.style.display = 'none';
    startCamera(currentHand);
}

function uploadPhotos() {
    const formData = new FormData();
    formData.append('rightHand', dataURItoBlob(rightHandImage), 'right_hand.jpg');
    formData.append('leftHand', dataURItoBlob(leftHandImage), 'left_hand.jpg');

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        // リセット
        rightHandImage = null;
        leftHandImage = null;
        uploadPhotosBtn.style.display = 'none';
    })
    .catch(error => {
        console.error('アップロードエラー:', error);
        alert('アップロードに失敗しました。');
    });
}

function dataURItoBlob(dataURI) {
    const byteString = atob(dataURI.split(',')[1]);
    const mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
    const ab = new ArrayBuffer(byteString.length);
    const ia = new Uint8Array(ab);
    for (let i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
    }
    return new Blob([ab], { type: mimeString });
}