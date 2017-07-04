import { Component } from '@angular/core';
import { Http, Headers } from '@angular/http';
import { ActionSheetController, ToastController, Platform, LoadingController, Loading } from 'ionic-angular';
import { URLSearchParams } from "@angular/http"

@Component({
    selector: 'page-addMessage',
    templateUrl: 'addMessage.html'
})
export class addMessage 
{
    message = {'from_id':'', 'to_id':'', 'msg':'' }
    
    loading: Loading;

    constructor(public http: Http, public toastCtrl: ToastController, public loadingCtrl: LoadingController) {}

    public logForm()
    {

    }

     private presentToast(text) {
        let toast = this.toastCtrl.create({
            message: text,
            duration: 3000,
            position: 'top'
        });
        toast.present();
    }

    public sendRequest()
    {
        this.loading = this.loadingCtrl.create({
            content: 'Uploading...',
        });
        this.loading.present();

        var apiUrl = 'http://192.168.100.5:5002/messanger';
        let headers = new Headers();

        var data = {
            'from_id':this.message.from_id,
            'to_id':this.message.to_id,
            'message': this.message.msg
        };
    
        let data2 = new URLSearchParams();
        data2.append('from_id', this.message.from_id);
        data2.append('to_id', this.message.to_id);
        data2.append('message', this.message.msg);
       // this.http.post(apiUrl, JSON.stringify(data), {headers: headers});
        this.http.post(apiUrl, data2)
          .subscribe(res => {
           
          }, (err) => {
            
          });
        this.loading.dismissAll()
        this.presentToast('Image succesful uploaded.');
       
    }
}