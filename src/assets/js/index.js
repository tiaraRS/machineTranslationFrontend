function name(){
    alert("This works")
}
translate_btn = document.getElementById("translate_btn")
translate_btn.addEventListener("submit", translate);
alert('translate_btn')
alert("hi")
translation_text_area = document.getElementById("input_txt")
output_translation_text_area = document.getElementById("input_txt")
function translate(event){
    event.preventDefault();
    let url = 'http://127.0.0.1:5002/';
    var text_for_translation = {            
        text:translation_text_area.value
    };

    var text_for_translation_Json = JSON.stringify(text_for_translation)
    alert('GET')
    fetch(url,{           
        method: 'GET'//,
        //body: text_for_translation_Json
    }).then((response) => {
        if (response.status === 200) {
            alert("si da");
            var data = await response.json();                      

            output_translation_text_area.value = data.translation
        } else {
            response.text().then((data) => {
                console.log(data);
            });
        }
    }).catch((response) => {
        console.log(data);
    });              
}