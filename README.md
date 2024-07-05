# 5001_puzzle

I have applied MVC design in this project, where M states the model, V states the view and C states the controller. 

Controller serves as the bridge between model and view. The controller inherit from both view and model classes.

Here, the onclick function is definitely the most vital part in this project. It calls the static function in model to get the required data and send that to the view to draw a picture or write down some text.

Furthermore, I applied staticmethod in the model class as they are just models, all the required data is stored in controller and the view. In other words, the model class serves as a library in my project.
