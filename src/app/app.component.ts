import { Component } from '@angular/core';
import {HttpClientModule} from '@angular/common/http';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})


export class AppComponent {
  private httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };
  constructor(private http: HttpClient){}
  text=""
  route='http://127.0.0.1:5002/eng_spa'
  source_language = "ENGLISH"
  target_language = "SPANISH"
  input_text_placeholder="Write text"

  public translate(text_for_translation:string){
    this.text = ""
    this.http.post<any>(this.route, {translation_text:text_for_translation},this.httpOptions).subscribe(data => {
          this.text = data.translation;
    })

  }
  
  onClick(text_for_translation:string) {
    
    this.translate(text_for_translation);
  }

  changeLanguage(){
    if (this.source_language == "ENGLISH"){
      this.source_language = "SPANISH";
      this.target_language = "ENGLISH";
      this.route='http://127.0.0.1:5002/spa_eng'
      this.input_text_placeholder="Escribe Texto";
    }
    else{
      this.source_language = "ENGLISH";
      this.target_language = "SPANISH";
      this.route='http://127.0.0.1:5002/eng_spa'
      this.input_text_placeholder="Write text";
    }
    this.text="";
  }
}