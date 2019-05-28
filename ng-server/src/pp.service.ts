import {Injectable, Input, OnChanges, SimpleChanges} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Observable, of, Subject} from "rxjs";
import {catchError, tap} from "rxjs/operators";

const httpOptions = {
  headers: new HttpHeaders({'Content-Type': 'application/json'})
};

export interface TableRow {
  parameter: string;
  value: number;
  categoryValue: number;
}

export interface ParagraphRow {
  index: number;
  score: number;
  value: string;
}

export interface PrivacyPolicy {
  table: TableRow[];
  paragraphs: ParagraphRow[];
  score: number;
}


@Injectable({
  providedIn: 'root'
})

export class PpService {
  privacyPolicyData = new Subject<Observable<PrivacyPolicy>>();
  serverUrl = 'http://127.0.0.1:5000/';
  progressBar: boolean = false;

  constructor(private http: HttpClient) {
  }

  getPrivacyPolicy(privacyPolicyUrl: string): void {
    const url = `pp-prediction?url=${privacyPolicyUrl}`;
    this.privacyPolicyData.next(this.http.get<PrivacyPolicy>(this.serverUrl + url, httpOptions).pipe(
      tap(() => console.log(`fetched privacy policy ${privacyPolicyUrl}`)),
      catchError(this.handleError<PrivacyPolicy>(`getPrivacyPolicy privacyPolicyUrl=${privacyPolicyUrl}`))
    ));
  }


  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {

      // TODO: send the error to remote logging infrastructure
      console.error(error); // log to console instead

      // TODO: better job of transforming error for user consumption
      console.log(`${operation} failed: ${error.message}`);


      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }
}
