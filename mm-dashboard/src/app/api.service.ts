import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AuthService } from './auth.service';


@Injectable()
export class APIService {

  headers = new HttpHeaders()
        .set('Authorization', 'Token ' + this._auth.getToken());

  constructor(private _http: HttpClient, private _auth: AuthService) { }

  postEvent(date, title, description){
    var payload = {
    	"date": date,
    	"title": title,
    	"description": description
    }

    this._http.post("http://localhost:8000/events/", payload, {headers:this.headers})
    	.subscribe(
	        res => {
	          console.log(res);
	        },
	        err => {
	          console.log("Error occured", err);
	        }
	    );
  }

  getDashboard(){
    return this._http.get("http://localhost:8000/dashboard/", {headers:this.headers})
  }

  simulateCompleteWorkSession() {
    this._http.get("http://localhost:8000/simulations/complete_work_session", {headers:this.headers})
      .subscribe(
          res => {
            console.log(res);
          },
          err => {
            console.log("Error occured", err);
          }
      );
  }

  simulateInCompleteWorkSession() {
    this._http.get("http://localhost:8000/simulations/incomplete_work_session", {headers:this.headers})
      .subscribe(
          res => {
            console.log(res);
          },
          err => {
            console.log("Error occured", err);
          }
      );
  }

  simulatePausedWorkSession() {
    this._http.get("http://localhost:8000/simulations/paused_work_session", {headers:this.headers})
      .subscribe(
          res => {
            console.log(res);
          },
          err => {
            console.log("Error occured", err);
          }
      );
  }

  simulateDailyComplete() {
    this._http.get("http://localhost:8000/simulations/daily_complete", {headers:this.headers})
      .subscribe(
          res => {
            console.log(res);
          },
          err => {
            console.log("Error occured", err);
          }
      );
  }

}
