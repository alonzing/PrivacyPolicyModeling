import {Injectable} from '@angular/core';
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

export interface Category {
  cat_key: string;
  name: string;
}

@Injectable({
  providedIn: 'root'
})

export class PpService {
  privacyPolicyData = new Subject<PrivacyPolicy>();
  serverUrl = 'http://127.0.0.1:5000/';
  progressBar: boolean = false;
  categories: Observable<Category[]>;

  constructor(private http: HttpClient) {
  }

  getPrivacyPolicy(privacyPolicyUrl: string, privacyPolicyCategory: string): Observable<PrivacyPolicy> {
    const command_name = `pp-prediction?`;
    const parameters = [`url=${privacyPolicyUrl}`, `category=${privacyPolicyCategory}`];

    return this.http.get<PrivacyPolicy>(`${this.serverUrl}${command_name}${parameters.join('&')}`, httpOptions).pipe(
      tap((privacyPolicy: PrivacyPolicy) => {
        console.log(`fetched privacy policy ${privacyPolicyUrl}`);
        this.privacyPolicyData.next(privacyPolicy);
      }),
      catchError(this.handleError<PrivacyPolicy>(`getPrivacyPolicy privacyPolicyUrl=${privacyPolicyUrl}`))
    );
  }

  getCategories(): Observable<string[]> {
    return this.http.get<string[]>(`${this.serverUrl}app-categories`, httpOptions).pipe(
      tap(() => {
        console.log(`fetched categories`);
      }),
      catchError(this.handleError<string[]>(`getCategories`))
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
