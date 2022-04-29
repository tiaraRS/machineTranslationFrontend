/*import { Component, OnInit } from '@angular/core';
declare var name:any
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  ngOnInit():void{
    new name();
  }
  title = 'MT';
}
*/

import { Component } from '@angular/core';
import {HttpClientModule} from '@angular/common/http';
import { HttpClient, HttpHeaders } from '@angular/common/http';
//declare const name:alert("This works")
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
  /*public alert_text(){
    alert(this.text)
  }*/
  public translate(text_for_translation:string){
    //alert(text_for_translation)
    /*this.http.get<any>('http://127.0.0.1:5002').subscribe(data => {
      this.text = data.translation;
    })*/
    this.text = ""
    this.http.post<any>('http://127.0.0.1:5002', {translation_text:text_for_translation},this.httpOptions).subscribe(data => {
          this.text = data.translation;
          //this.alert_text()
    })

  }
/*this.alert_text()
    this.http.post<any>('http://127.0.0.1:5002', { translation_text: 'Angular POST Request Example' }).subscribe(data => {
          this.text = data.translation;
      })
    this.alert_text()
  }*/
  
  onClick(text_for_translation:string) {
    
    this.translate(text_for_translation);
  }
}


/*import { Component, OnInit } from '@angular/core';
declare var name:any
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  ngOnInit():void{
    new name();
  }
  title = 'MT';
}
*/


/*
export class AppComponent {
  private httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  constructor(private http: HttpClient) { }
  title = 'Angular Tutorial';
  text=""
  
  public name(){

    this.http.post<any>('https://reqres.in/api/posts', { title: 'Angular POST Request Example' }).subscribe(data => {
          this.text = data.id;
      })
  }
  onClick() {
    this.name();
  }
}*/