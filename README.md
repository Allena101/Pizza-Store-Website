# Pizza-store Final

This is for ¤ Pizza Final

Here are some instructions and thoughts regarding this Pizza project.

First of all, in order to log in as admin you have to use the email that is: sten@sten.com and password is: lösen. Sten has User.id of 4 which grants him access to the register route.

The idea is that the boss or admin adds employees so he decides the password and username for his employees (which happens at some work places). The customer can reach login page but cannot log in and employees can reach register page butt they will be redirected since they are not an admin/boss. . I did not add the functionally for the employees to change their account info, which i would have had if i had more time. At least password change should be a feature.

Cleaning up the code the last few days created a bug where the user is logged out sometimes that i did not have the time to figure out. There might also be some bugs related to deleting toppings that a pizza uses that i just thought of.

So the idea behind the site is that the user does not create an account and only uses the home page. Where the user orders pizza and selects a size. This generates an order that is listed in the sidebar. When the user is done selecting pizza he orders and then the order is sent to the OrderHistory page which the employees can see and they can start to prepare the pizzas. This is of course a simplification of how it would work in real life.

Some functions include that the pizza topping stock is monitored so that pizzas that don't have enough topping will be shown as: out of stock.

The site has pages for adding whole pizzas and toppings as well as removing pizzas and toppings. As well as changing the stock/inventory status for toppings. Which allows employees to change topping status dynamically so that the customers cannot order a pizza with a topping they just ran out of due to high demand.

The orderHistory page is meant for employees to see incoming orders so that they can prepare those pizzas. The orders are grouped with order id so they know which customer ordered which pizza.

Without a doubt this project can be improved tremendously and there is still room for more important features. However, the essential CRUD functionality is implemented (adding and removing pizzas/toppings). Functionality where customers, employees, and admin has access to different parts of the site: (e.g. only Admin can reach the register page where he can add new employees and users that are not logged in (customers) can only reach the order pizza page), works well but still room for improvement.

Magnus Jensen
