import { Injectable } from '@angular/core';
import { Http, Headers } from '@angular/http';
import 'rxjs/add/operator/map';

let apiUrl = 'http://localhost:1337/localhost:8080/api/';

@Injectable()
export class AuthService {

  constructor(public http: Http) {}

  login(credentials) {
    //return new Promise((resolve, reject) => {
        //let headers = new Headers();
        //headers.append('Content-Type', 'application/json');
        
        /*this.http.post(apiUrl+'login', JSON.stringify(credentials), {headers: headers})
          .subscribe(res => {
            resolve(res.json());
          }, (err) => {
            reject(err);
          });*/
    //});
    if(credentials.username=="test" && credentials.password=="test") return Promise.resolve({"access_token": "1234"});
    else return new Promise((resolve, reject) => {reject('Invalid credentials!')});
 }

  register(data) {
    return new Promise((resolve, reject) => {
        let headers = new Headers();
        headers.append('Content-Type', 'application/json');

        this.http.post(apiUrl+'guest/signup', JSON.stringify(data), {headers: headers})
          .subscribe(res => {
            resolve(res.json());
          }, (err) => {
            reject(err);
          });
    });
  }

  logout(){
    /*return new Promise((resolve, reject) => {
        let headers = new Headers();
        headers.append('X-Auth-Token', localStorage.getItem('token'));

        this.http.post(apiUrl+'logout', {}, {headers: headers})
          .subscribe(res => {
            localStorage.clear();
          }, (err) => {
            reject(err);
          });
    });*/

    return Promise.resolve(localStorage.clear());
  }

}
