import axios from 'axios';


export const globalFunctions = {
    httpRequest: (type, url, formData=undefined, auth=false, zip_file=false, multipart=false) => {
        let parameters = {
            "headers": {}
        }

        if(auth){
            parameters.headers['Authorization'] = `Token ${localStorage.getItem('mapping_portal_access_token')}`
        }

        if(zip_file){
            parameters.responseType = 'blob'
        }

        if(multipart){
            parameters.headers['Content-Type'] = 'multipart/form-data'
        }

        return new Promise((resolve) => {
            if(type === 'get'){
                axios.get(url, parameters).then((response) => {
                    resolve(response)
                })
                .catch(error => {
                    if('response' in error) {
                        if(error.response === undefined){
                            resolve(error)
                        }
                        if(error.response.status != '401'){
                            resolve(error.response)
                        }
                    } else {
                        resolve(error)
                    }
                })
            }else if(type === 'post'){
                axios.post(url, formData, parameters).then((response) => {
                    resolve(response)
                })
                .catch(error => {
                    if('response' in error) {
                        if(error.response === undefined){
                            resolve(error)
                        }
                        if(error.response.status != '401'){
                            resolve(error.response)
                        }
                    } else {
                        resolve(error)
                    }
                })
            }else if(type === 'put'){
                axios.put(url, formData, parameters).then((response) => {
                    resolve(response)
                })
                .catch(error => {
                    if('response' in error) {
                        if(error.response === undefined){
                            resolve(error)
                        }
                        if(error.response.status != '401'){
                            resolve(error.response)
                        }
                    } else {
                        resolve(error)
                    }
                })
            }else if(type === 'delete'){
                axios.delete(url, {formData,...parameters}).then((response) => {
                    resolve(response)
                })
                .catch(error => {
                    if('response' in error) {
                        if(error.response === undefined){
                            resolve(error)
                        }
                        if(error.response.status != '401'){
                            resolve(error.response)
                        }
                    } else {
                        resolve(error)
                    }
                })
            }
        })
    }
}