import { Component, OnInit, VERSION } from "@angular/core";
import { environment } from './../../environments/environment';
import {NotificationsService} from 'angular2-notifications';

import {
  HttpClientModule,
  HttpClient,
  HttpRequest,
  HttpResponse,
  HttpEventType,
  HttpHeaders,
} from "@angular/common/http";
import { Router } from "@angular/router";




@Component({
  selector: "app-table-list",
  templateUrl: "./table-list.component.html",
  styleUrls: ["./table-list.component.css"],
})
export class TableListComponent implements OnInit {
  //Filtering
  ProfileType: string;
  Name: any;
  //pagination
  p: Number = 1;
  totalRecord: Number;
  //Sorting
  key: string = "Experience";
  reverse: boolean = false;
 
  //getdata
  result: any;
  response: any;
  
  //deletedata
   resultdelete: any;
   filedelete: any;
 
  //Sorting
  sort(key) {
    this.key = key;
    this.reverse = !this.reverse;
  }

  //get path
   path: string='';
  
  //environment variable
   environmentVar= environment.SpringEndPoint; 
  
    resultdown: any;
    fileName: string;

  //get data from ES
  getdata(){
    this.http.get(environment.ElasticseachEndPoint+"/test1/cv/_search?pretty")
    .subscribe(result=> {
      this.result = result;
      this.response= this.result.hits.hits;
      this.path= this.response?._source?.pathpdf;
      console.log(this.response);
      })
  }
  //delete data in ES
  deleteDocument(a:string, i:number, name: string){
    this.http.delete(environment.ElasticseachEndPoint+'/test1/cv/'+a).subscribe(resultdelete=>{this.resultdelete=resultdelete;
          });
     this.response.splice(i, 1);   
     this.http.get(environment.SpringEndPoint+'/delete/'+name).subscribe(filedelete=>{this.filedelete=filedelete;
     });
     this.onSuccess('Profile deleted succefully');  

      }

  onSubmit(){
    this.routing.navigateByUrl('/user-profile');
  }
    
  constructor(private http: HttpClient, private routing : Router, private servicetable: NotificationsService) {
    }
  

  ngOnInit() {
    return this.getdata();
    
  }
  onSuccess(message){
    this.servicetable.success( 'Sucess', message , {position: ['bottom', 'left' ],
                                                  timeOut: 2500,
                                                animate: 'fade',
                                              showProgressBar: true})
      }

   
}
