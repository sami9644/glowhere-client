function bookService(serviceid,userid){
document.getElementsByName('serviceid')[0].value = serviceid
document.querySelector('.booking-form').style.display='block';
}

function unbookService(bookingid) {
if (confirm('Do you really want to unbook this?')) {
fetch(`/unbook/${bookingid}`)
.then(res => {
    if (!res.ok) {
        alert("Connection problem!")
    }
    else {
    return res.json()
    }
})
.then(data => {
    alert(data.message)
    location.reload()
})
.catch(err => {
    alert(err.message)
})
}
}