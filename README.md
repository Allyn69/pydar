# Real-Time Flight Radar

Live flight tracking terminal app written in Python. All you need to provide is a point from which you want to observe.  Relax and observe planes above your head!

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites
You need to install pyhton packages listed in requirements.txt

```
Cartopy
geopy
requests
matplotlib
```
### Installing

A step by step series of examples that tell you how to get a development env running

Clone the repository.

```
git clone https://github.com/QuarKUS7/airport_radar.git
```
Install prerequisites

```
cd pydar
pip install -r ./requirements.txt
```
Now try the Pydar...

Run pydar.py **latitude** **longitude** of a point you want to observe

For example this command will observe Vaclav Havel Airport in Prague
```
python pydar.py 50.100499598 14.255998976
```

## Deployment

Docker here

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Peter Pagac** - (pagac.peter123@gmail.com)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
