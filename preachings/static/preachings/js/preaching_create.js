let tagCounter = 0;
let formValueArray = new Array();
let data = {}
let tagFormValue = [];
//ToDo: add the value of formValueArray to the hidden form from django. 
// Also do the delete to delete the array content then replace again the value of form hidden from django

//AJAX
document.addEventListener('DOMContentLoaded', function() {

   document.getElementById('id_tag').onkeyup = function(e){
        let keyword = document.getElementById('id_tag').value;
        let tagSuggestionList = document.getElementById("tag_list");
       // initialize new request
       const request = new XMLHttpRequest();
       request.open("POST", "/note/add/tag");
        
       data = {"keyword": keyword.trim()};

       if(!keyword){
        while(tagSuggestionList.lastChild){
            tagSuggestionList.removeChild(tagSuggestionList.lastChild);
        }
    }
       //when request is finished
       request.onload = () => {
            const data = JSON.parse(request.responseText);
            let keyword = document.getElementById('id_tags').value;
            let tagSuggestionList = document.getElementById("tag_list");

            console.log(formValueArray);

            while(tagSuggestionList.lastChild){
                tagSuggestionList.removeChild(tagSuggestionList.lastChild);
            }
            let li_1 = document.createElement('li');
            li_1.setAttribute('class', 'bg-dark text-white p-2')
            li_1.textContent = 'Suggestions: '
            tagSuggestionList.appendChild(li_1);
            for(let tag of data.tag){
                let li_2 = document.createElement('li');
                let spanLi2 = document.createElement('span');
                spanLi2.textContent = 'Add Tag';
                spanLi2.setAttribute('class', 'btn btn-info ml-2 p-2');
                li_2.setAttribute('class', 'border bg-light p-2 ');
                spanLi2.setAttribute('name', tag);
                spanLi2.setAttribute('onClick', 'suggestionAddTag(\'' + tag + '\')');
                li_2.textContent = tag;
                li_2.append(spanLi2);
                tagSuggestionList.appendChild(li_2);
                
            }
            return false;
       }
       
       request.setRequestHeader("Content-Type", 'application/json;');
       request.setRequestHeader("X-CSRFToken", csrftoken);
       
       if(data['keyword']){
        request.send(JSON.stringify(data));
       }
            
       
   };

});

function deleteTag(){
    this.parentNode.remove();
}  


function suggestionAddTag(tag){
    let li = document.createElement('li');
    li.setAttribute('class', 'list-inline-item  m-3');
    li.setAttribute('id', tag);
    let spanLi2 = document.createElement('span');
    spanLi2.textContent = tag;
    spanLi2.setAttribute('class', 'bg-dark text-white p-2 ');
    spanLi2.setAttribute('name', 'tags');
    let spanli3 = document.createElement('span');
    spanli3.textContent = 'X';
    spanli3.setAttribute('class', 'bg-danger ml-0 p-2 text-white')
    spanli3.setAttribute('onClick', 'remove(\'' + tag + '\')');
    li.appendChild(spanLi2);
    li.appendChild(spanli3);
    formValueArray.push(tag);
    document.getElementById('id_tags').value = formValueArray.join(',');
    document.getElementById('tag_list_final').appendChild(li);

}

function addTag(){
    let value = document.getElementById('id_tag').value;
    let li = document.createElement('li');
    li.setAttribute('class', 'list-inline-item m-3');
    li.setAttribute('id', value);
    let spanLi2 = document.createElement('span');
    spanLi2.textContent = value;
    spanLi2.setAttribute('class', 'bg-dark text-white p-2 mt-2');
    spanLi2.setAttribute('name', 'tags');
    let spanli3 = document.createElement('span');
    spanli3.textContent = 'X';
    spanli3.setAttribute('onClick', 'remove(\'' + value + '\')');
    spanli3.setAttribute('class', 'bg-danger ml-0 p-2 text-white')
    li.appendChild(spanLi2);
    li.appendChild(spanli3);
    formValueArray.push(value);
    document.getElementById('id_tags').value = formValueArray.join(',');
    document.getElementById('tag_list_final').appendChild(li);
}

function remove(tag){
    formValueArray.splice(formValueArray.indexOf(tag), 1);
    document.getElementById('id_tags').value = formValueArray.join(',');
    let node = document.getElementById(tag);
    document.getElementById('tag_list_final').removeChild(node);
}


/*
Sample Output:
Counsel, Jesus Christ, Resurrection, Decision

So the input is either suggested or entered. 

1. the form input can be sent plainly because it can be split in python

The problem:
1. Get suggestions from database based on each tag delimeted with comma 

- While typing, get suggestions - /

- after a comma, get suggestions for the word after comma 
    I need to access each comma separated word 

    Counsel, 

    focus on suggesting tags on the words after comma 
    What about if there's no comma yet


    Lets understand some reg ex patterns first 



*/