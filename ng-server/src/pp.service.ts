import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Observable, of} from "rxjs";
import {catchError, tap} from "rxjs/operators";
const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

export interface TableRow {
  parameter: string;
  value: number;
  categoryValue: number;
}
export interface PrivacyPolicy {
  table: TableRow[];
  appCategory: string;
  devUrl: string;
  numOfParagraphs: number;
  numOfTopics: number;
  numOfMissingParagraphs: number;
  numOfParagraphsCategoryValue: number;
  numOfMissingParagraphsCategoryValue: number;
  numOfTopicsCategoryValue: number;
  score: number;
  paragraphs: string[];
}



@Injectable({
  providedIn: 'root'
})

export class PpService {
  privacyPolicyData: PrivacyPolicy;
  serverUrl = 'http://127.0.0.1:5000/';
  progressBar: boolean = false;
  constructor(private http: HttpClient) { }

  getPrivacyPolicy(privacyPolicyUrl: string): Observable<PrivacyPolicy> {
    const url = `pp-prediction?url=${privacyPolicyUrl}`;
    return this.http.get<PrivacyPolicy>(this.serverUrl + url,httpOptions).pipe(
      tap(() => console.log(`fetched privacy policy ${privacyPolicyUrl}`)),
      catchError(this.handleError<PrivacyPolicy>(`getPrivacyPolicy privacyPolicyUrl=${privacyPolicyUrl}`))
    );
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
