import { BaseOverlayDispatcher } from "@angular/cdk/overlay/dispatchers/base-overlay-dispatcher";
import { Basics } from "./Basics";
import { WorkingExperience } from "./WorkingExperience";

export class CV {
  public basics: Basics = new Basics();
  public numberOfYears: number ;
  public work_experience: WorkingExperience[];
  public skills: string[];
  public pdfName: string;
  public technicalcompetence: string;
  public functionalcompetence: string;
  public parsedExperience: string;
  public education_and_training : string[];
  public education: string;
  public accomplishments: string[];
  public certifications: string;
  constructor(){
    
}



}
