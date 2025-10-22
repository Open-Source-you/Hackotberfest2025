function generateQRcode(){
    const qrInput= document.getElementById("qrInput").value.trim();
    const qrImage= document.getElementById("qrcodeimage")
if(qrInput==""){
    alert("Please enter text or URL to generate QR code");
    return;
}
const apiURL=`https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(qrInput)}`;
qrImage.src= apiURL;
}
