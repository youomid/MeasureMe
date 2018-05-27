import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';


@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private _http: HttpClient) { }

  login(username, password){
  	var payload = {
    	"username": username,
    	"password": password
    }

    return this._http.post("http://localhost:8000/rest-auth/login/", payload);
  }

  logout(){
  }

  validateToken(authToken){
  	var headers = new HttpHeaders()
        .set('Authorization', 'Token ' + this.getToken());
    return this._http.get("http://localhost:8000/rest-auth/user/", {headers:headers})
  }

  getToken(){
  	return localStorage.getItem('authToken');
  }

  storeToken(authToken){
  	localStorage.setItem('authToken', authToken)
  }

}
