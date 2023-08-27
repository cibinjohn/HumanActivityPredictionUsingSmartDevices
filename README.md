# HumanActivityPredictionUsingSmartDevices
# Introduction 
TODO: API to predict human activity from smart devices

## Getting Started
# Environment Variables:

1. MODEL_PATH
2. PORT
3. HOST
4. LOGFILE

# Setting up kubernetes cluster using Minikube.

1. Install minikube with docker in local
2. To start minikube in the local, open linux terminal and run the following command.
      ```
      minikube start
      ```
3. To open the minikube dashboard, run the following command in the terminal.
      ```
      minikube dashboard
      ```
  You can monitor the status of the deployments, pods, and services here.  It also provides you the option to check the logs of the pods, and enter their consoles
  
4. Deploy the pods.  Run the following command in the terminal to set up the services.
```
./setup_kubernetes.sh
```
5. The above command will initiate the deployment process, and monitor the stauts of the pods.  Once the pods are in running condition, run the following command in the terminal to set up the services.  This will auto direct you to the application. 
    ```
    ./setup_services.sh
    ```
6. To remove all the services, pods, deployments, secrets and config, run the following command in the terminal.
    ```
    ./reset_kubernetes.sh
    ```

# Sample request(PUT)

```
{"smartdevices_data":[{"timestamp": "2017-07-12 12:23:00",
  "pressure": 980.1421,
  "ACC_X": 0.16765137,
  "ACC_Y": 0.98195803,
  "ACC_Z": 9.946517,
  "GRAVITY_X": -0.05498579,
  "GRAVITY_Y": 0.9446233,
  "GRAVITY_Z": 9.760894,
  "GYRO_X": 0.00023740018,
  "GYRO_Y": -0.00013840524,
  "GYRO_Z": -0.000749876,
  "LA_X": 0.22610946,
  "LA_Y": 0.057997074,
  "LA_Z": 0.17573905,
  "MAG_X": 5.9478207,
  "MAG_Y": -2.3263187,
  "MAG_Z": -20.610098,
  "ORI_X": -98.79417841938223,
  "ORI_Y": -5.711082738186849,
  "ORI_Z": -1.007992380799606,
  "AUDIO_W": 120.6,
  "AUDIO_X": 1330.80632,
  "AUDIO_Y": 32767.0,
  "AUDIO_Z": 37.0,
  "ROTATION_VECTOR_A": 0.07323526,
  "ROTATION_VECTOR_B": 0.02294765,
  "ROTATION_VECTOR_C": 0.7300451,
  "ROTATION_VECTOR_D": 0.67907596,
  "ROTATION_VECTOR_E": 0.5235988},
 {"timestamp": "2017-07-12 12:23:05",
  "pressure": 980.1657,
  "ACC_X": 0.16046631,
  "ACC_Y": 0.9915381,
  "ACC_Z": 9.939331,
  "GRAVITY_X": -0.044430897,
  "GRAVITY_Y": 0.9422843,
  "GRAVITY_Z": 9.761174,
  "GYRO_X": -0.0003837105,
  "GYRO_Y": -0.0006421283,
  "GYRO_Z": 0.0007183675,
  "LA_X": 0.21094044,
  "LA_Y": 0.05493419,
  "LA_Z": 0.17544854,
  "MAG_X": 6.6978207,
  "MAG_Y": -2.7013187,
  "MAG_Z": -21.860098,
  "ORI_X": -87.97417522684155,
  "ORI_Y": -5.707043961953255,
  "ORI_Z": -0.9682091969269264,
  "AUDIO_W": 96.4,
  "AUDIO_X": 1330.1659,
  "AUDIO_Y": 32767.0,
  "AUDIO_Z": 37.0,
  "ROTATION_VECTOR_A": 0.07315441,
  "ROTATION_VECTOR_B": 0.022346666,
  "ROTATION_VECTOR_C": 0.73350227,
  "ROTATION_VECTOR_D": 0.67536914,
  "ROTATION_VECTOR_E": 0.5235988},
 {"timestamp": "2017-07-12 12:23:10",
  "pressure": 980.15045,
  "ACC_X": 0.16286133,
  "ACC_Y": 0.98435307,
  "ACC_Z": 9.934542,
  "GRAVITY_X": -0.035401825,
  "GRAVITY_Y": 0.9429927,
  "GRAVITY_Z": 9.761142,
  "GYRO_X": 0.0013263177,
  "GYRO_Y": 0.0003583096,
  "GYRO_Z": -0.0007971814,
  "LA_X": 0.19174643,
  "LA_Y": 0.05048069,
  "LA_Z": 0.16600858,
  "MAG_X": 5.9478207,
  "MAG_Y": -3.4513187,
  "MAG_Z": -21.485098,
  "ORI_X": -98.44006043167376,
  "ORI_Y": -5.679721924612736,
  "ORI_Z": -0.9267218808563285,
  "AUDIO_W": 113.6,
  "AUDIO_X": 1329.52938,
  "AUDIO_Y": 32767.0,
  "AUDIO_Z": 37.0,
  "ROTATION_VECTOR_A": 0.0730299,
  "ROTATION_VECTOR_B": 0.022295102,
  "ROTATION_VECTOR_C": 0.7377355,
  "ROTATION_VECTOR_D": 0.67075765,
  "ROTATION_VECTOR_E": 0.5235988},
 {"timestamp": "2017-07-12 12:23:15",
  "pressure": 980.1437,
  "ACC_X": 0.16046631,
  "ACC_Y": 0.98435307,
  "ACC_Z": 9.932146,
  "GRAVITY_X": -0.023846995,
  "GRAVITY_Y": 0.94340914,
  "GRAVITY_Z": 9.761137,
  "GYRO_X": -0.0018913767,
  "GYRO_Y": 0.0008103468,
  "GYRO_Z": 0.0007840707,
  "LA_X": 0.19264105,
  "LA_Y": 0.036941245,
  "LA_Z": 0.16948761,
  "MAG_X": 5.9478207,
  "MAG_Y": -4.2013187,
  "MAG_Z": -20.610098,
  "ORI_X": -101.21081546094864,
  "ORI_Y": -5.665981718436785,
  "ORI_Z": -0.954380198291766,
  "AUDIO_W": 117.8,
  "AUDIO_X": 1328.89862,
  "AUDIO_Y": 32767.0,
  "AUDIO_Z": 37.0,
  "ROTATION_VECTOR_A": 0.07284546,
  "ROTATION_VECTOR_B": 0.02229957,
  "ROTATION_VECTOR_C": 0.7417381,
  "ROTATION_VECTOR_D": 0.66634893,
  "ROTATION_VECTOR_E": 0.5235988},
 {"timestamp": "2017-07-12 12:23:20",
  "pressure": 980.2219,
  "ACC_X": 0.16525635,
  "ACC_Y": 0.99393314,
  "ACC_Z": 9.939331,
  "GRAVITY_X": -0.0099347895,
  "GRAVITY_Y": 0.9467973,
  "GRAVITY_Z": 9.760833,
  "GYRO_X": 0.0007674041,
  "GYRO_Y": 0.000848891,
  "GYRO_Z": -0.0003626647,
  "LA_X": 0.17083262,
  "LA_Y": 0.052075535,
  "LA_Z": 0.16650434,
  "MAG_X": 5.9478207,
  "MAG_Y": -3.0763187,
  "MAG_Z": -20.610098,
  "ORI_X": -98.95574654419887,
  "ORI_Y": -5.670083247033378,
  "ORI_Z": -0.941232831191432,
  "AUDIO_W": 178.0,
  "AUDIO_X": 1328.27392,
  "AUDIO_Y": 32767.0,
  "AUDIO_Z": 37.0,
  "ROTATION_VECTOR_A": 0.07261588,
  "ROTATION_VECTOR_B": 0.022254948,
  "ROTATION_VECTOR_C": 0.7443974,
  "ROTATION_VECTOR_D": 0.66340345,
  "ROTATION_VECTOR_E": 0.5235988}]}


```

# SAMPLE RESPONSE
```
{
    "results": [
        {
            "timestamp": "2017-07-12 12:23:00",
            "prediction": "In computer"
        },
        {
            "timestamp": "2017-07-12 12:23:05",
            "prediction": "In computer"
        },
        {
            "timestamp": "2017-07-12 12:23:10",
            "prediction": "In computer"
        },
        {
            "timestamp": "2017-07-12 12:23:15",
            "prediction": "In computer"
        },
        {
            "timestamp": "2017-07-12 12:23:20",
            "prediction": "In computer"
        }
    ],
    "code": 200,
    "message": "Human activities predicted successfully"
}
```
