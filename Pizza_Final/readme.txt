Here are some instructiosn and thoughts regarding this Pizza project.

I fidn it easer to code in english since that is waht i am reading all the time and the concepts are all in english and i thinkg its uggly to mix to swedish and english back and forth or translate concepts on the fly. Since i did not find a requiremetn for the pizza website to be in sweidish i decied to make it in english since we are usually engourged to be global and it also fits with me coding in egnlish. Hope this is not an issue.

First of all, in order to log in as admin you have to use the email that is  sven@sven.com and passwrod is: lösen. Sven has User.id of 4 which grants him access to the register route. 

The idea is that the boss or admin adds employees so he decides the passwrod and username for his employees (which happens at some work places). The customer can reach login page but cannot log in and employees can reach register page butt they will be redirected since they are not an admin/boss. . I did not add the fucntinalty for the employess to change theri account info, which i would have had if i had more time. At least password change should be a feature. 

There is definietly a way to make a site where the user cannot see any link but the employees can still log in. I did not find how this is done , one guess is that a button is not there and the employee has to type in the url but that sounds incorrect.

Cleaning up the code the last few days created a bug where the user is logged out sometiems that i did not have the time to figure out. There might also be some bugs related to deleting toppings that a pizza uses that i just thought of.

So the idea behind the site is that the user does not create an account and only uses the home page. Where the user orders pizza and selects a size. This generates an order that is listed in the sidebar. When the user is done selecting pizza he orders and then the order is sent to the OrderHistory page which the employess can see and they can start to prepare the pizzas. of course this is a simplification of how it would work in real life. 

Some functions include that the pizza topping stock is montitored so that pizzas that dont have enough topping will be shown as read and out of stock. 

The site has pages for adding whole pizzas and toppings as well as removing pizzas and toppings. As well as chagnign the stock/inventory status for toppings. So that the employees can change topping status dynamically so that the customers cannot order a pizza with a topping they just ran out of due to high demand.

of course you could add fucntionality related to chagnign pizzas but i only have fucntioanltiy related to ading or deleting a whole pizza. 

The orderHistory page is meant for employees to see incoming orders so that they can make those pizzas. The orders are grouped with order id so they know which customer orderd which pizza. 

The css is a mess, which i metnion in the code. And the styling did turn out pretty uggly, but at least it is pretty clear and minilaistic, which i like. My eye sight very bad (got congential eye issues that are not just near sightedness) so i alwasy zoom in on website , which have made me predisposed to design a website where everything is bigger than perhaps the standard user can apprecaite. I would need to test this on other users that dont have impared eye sight.

to end this i am satisfied that i manage to create the important funcitnality , even more satisfied since i encountered several obstibles where i got stuck or had to redo things or change direction.

sorry for not adding a requirments.txt file

httpsgithub.comAllena101Pizza-Store-BBB

Magnus Jensen

