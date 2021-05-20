import { Component, OnInit } from "@angular/core";
import {
  HttpClient,
  HttpResponse,
  HttpEventType,
} from "@angular/common/http";
import {WorkingExperience} from "app/Model/WorkingExperience";
import { CV } from "app/Model/CV";
import { HttpHeaders } from "@angular/common/http";
import { ActivatedRoute, Router } from "@angular/router";
import {NotificationsService} from 'angular2-notifications';
import { environment } from './../../environments/environment';
import { single } from "./data";

@Component({
  selector: "app-user-profile",
  templateUrl: "./user-profile.component.html",
  styleUrls: ["./user-profile.component.css"],
})
export class UserProfileComponent implements OnInit {
  //Upload File variable
  percentDone: number;
  uploadSuccess: boolean;
  resultfile: File;
  fileName: string;
  isfileLoaded: boolean = false;

  cvFile: CV = {
    pdfName: "",
    numberOfYears: null,
    work_experience: [],
    skills: [],
    technicalcompetence: "",
    functionalcompetence: "",
    education_and_training: [],
    parsedExperience: "",
    education: "",
    accomplishments: [],
    certifications: "",
    basics: {
      titre: "",
      name: { firstName: "", surname: "", middleName: "" },
      email: "",
      phone: null,
      adresse: "",
      url: "",
    },
  };
  //SS
  single: any[];
  view: any[];
  displayChart = false;
  // options
  gradient: boolean = true;
  showLegend: boolean = true;
  showLabels: boolean = true;
  isDoughnut: boolean = false;
  legendPosition: string = "below";

  colorScheme = {
    domain: ["#5AA454", "#A10A28", "#C7B42C", "#AAAAAA"],
  };

  //SS
  src: string = "";
  //parse variable
  public result: any;
  finalresult: any;
  file1: File;

  public response: any;
  id: string;
  event: any;

  showMsg: boolean = false;
  title = "notificationappYT";
  resultconcat: string;
  responsefinal: any;

  isLoaded: Boolean = false;
  skill;
  eduQ;
  certif: any[];
  responseget: string;

  constructor(
    private http: HttpClient,
    private activatedRoute: ActivatedRoute,
    private router: Router,
    private service: NotificationsService
  ) {
    Object.assign(this, { single });
  }

  ngOnInit() {
    this.id = this.activatedRoute.snapshot.paramMap.get("id");
    if (this.id != null) {
      this.editProfile(this.id);
    }
  }

  //Upload File
  upload(file: File[]) {
    this.uploadAndProgress(file);
    this.isfileLoaded = true;
  }

  //upload several files
  uploadAndProgress(files: File[]) {
    var reader = new FileReader();
    reader.readAsDataURL(files[0]);
    this.fileName = files[0].name;
    reader.onload = (event: any) => {
      this.src = event.target.result;
    };

    this.file1 = files[0];

    var formData = new FormData();
    Array.from(files).forEach((f) => formData.append("file", f));

    this.http
      .post("https://file.io", formData, {
        reportProgress: true,
        observe: "events",
      })
      .subscribe((event) => {
        if (event.type === HttpEventType.UploadProgress) {
          this.percentDone = Math.round((100 * event.loaded) / event.total);
        } else if (event instanceof HttpResponse) {
          this.onSuccessUpload("Upload Successful");
        }
      });
  }

  //parse file
  parse() {
    console.log("parsing");
    this.isLoaded = true;
    this.cvFile = new CV();
    var formData = new FormData();
    formData.append("resume", this.file1);
    return this.http
      .post(environment.SpringEndPoint + "upload/", formData, {
        responseType: "json",
      })
      .subscribe((result) => {
        this.result = result;
        this.isLoaded = false;
        this.finalresult = JSON.parse(JSON.stringify(result)).data;
        var extracted = result["extracted"];
        //this.cvFile = Object.assign({}, this.finalresult);

        this.cvFile.pdfName = this.fileName;
        var competences = extracted["Competences"];
        this.eduQ = this.cvFile.education_and_training;
        this.certif = this.cvFile.accomplishments;
        //ss
        this.cvFile.numberOfYears = extracted["Experience"];
        this.cvFile.basics.name.firstName = extracted["Nom"];
        this.cvFile.basics.name.surname = extracted["Prenom"];

        this.cvFile.basics.email = extracted["Email"];
        this.cvFile.basics.adresse = extracted["Adresse"];
        this.cvFile.basics.phone = extracted["Telephone"];
        this.single = extracted['Scores'];
        this.cvFile.basics.titre = extracted['Profil'];
        var parcours = extracted["Parcours"];
        this.cvFile.education = extracted['Education'];
        this.displayChart = true;

        if (competences != null) {
          var content = "";
          for (var key in competences) {
            //iterate each category
            var record = competences[key];
            content += record["category"] + ": ";
            var recordSkills = record["skills"];
            for (var i = 0; i < recordSkills.length; i++) {
              content += recordSkills[i];
              if (i == recordSkills.length - 1) continue;
              content += ",";
            }
            content += "\n";
            this.cvFile.technicalcompetence = content;
            //
            // console.log(competences);
            //this.cvFile.technicalcompetence = this.skill[0][key];
          }
        }
        if (parcours != null) {
          var content = "";
          console.log(parcours)
          for (var line in parcours) {
            //iterate each category
            content += parcours[line] + "\n";
            //
  
          }
          this.cvFile.parsedExperience = content;

        }
        /*
        if (this.eduQ != null) {
          for (var key in this.eduQ[0]) {
            this.cvFile.education = this.eduQ[0][key];
            console.log(this.cvFile.education);
          }
        }

        if (this.certif != null) {
          for (var key in this.certif[0]) {
            this.cvFile.certifications = this.certif[0][key];
            console.log(this.cvFile.certifications);
          }
        }*/
      });
  }

  //add Experience
  addExperience() {
    this.cvFile.work_experience.push(new WorkingExperience());
    //console.log(this.finalresult.work_experience);
  }
  //remove experience
  removeExperience(i: number) {
    this.cvFile.work_experience.splice(i, 1);
  }
  //submit form
  submit() {
    let headers: HttpHeaders = new HttpHeaders();
    headers.append("Content-Type", "application/json");
    console.log(this.cvFile);
    this.http
      .post(
        environment.ElasticseachEndPoint + "/test1/cv/" + this.id,
        this.cvFile,
        { headers }
      )
      .subscribe((event) => {
        console.log(event);
        this.onSuccessUpload("Profile created/edited succefully");
      });
  }

  editProfile(a: string) {
    this.http
      .get(environment.ElasticseachEndPoint + "/test1/cv/" + a)
      .subscribe((response) => {
        this.responsefinal = response;
        this.response = this.responsefinal._source;
        this.cvFile = Object.assign({}, this.response);
        console.log(this.cvFile);
        this.src =
          "C:UsersYosraeclipse-workspace\resume-parsersrcmain\resourcesResumesMohamed_Karim_Chaabane_Resume.pdf";
        console.log(this.src);
      });
  }
  onSuccess(message) {
    this.service.success("Sucess", message, {
      position: ["bottom", "left"],
      timeOut: 2500,
      animate: "fade",
      showProgressBar: true,
    });
  }
  onSuccessUpload(message) {
    this.service.success("Sucess", message, {
      position: ["up", "right"],
      timeOut: 2000,
      animate: "fade",
      showProgressBar: false,
    });
  }

  onError(message) {
    this.service.error("Error", message, {
      position: ["up", "right"],
      timeOut: 2500,
      animate: "fade",
      showProgressBar: false,
    });
  }
  onSelect(data): void {
    console.log("Item clicked", JSON.parse(JSON.stringify(data)));
  }

  onActivate(data): void {
    console.log("Activate", JSON.parse(JSON.stringify(data)));
  }

  onDeactivate(data): void {
    console.log("Deactivate", JSON.parse(JSON.stringify(data)));
  }
}