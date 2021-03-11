# DJINN
<a href="https://djinn.azurewebsites.net/">djinn.azurewebsites.net</a>
<br />
Incident management tool created with Python 3.8 and Django to learn coding again, because it's always useful.
<br />
<ul>
  The main module is composed by:
  <li>Django 3</li>
  <li>Bootstrap 4</li>
  <li>PostgreSQL 12</li>
  <li>JQuery 3.5</li>
</ul>
<ul>
  For the on-demand chat rooms module I added:
  <li>Django Rest Framework 3.11</li>
  <li>Channels 2.4</li>
  <li>Redis (previously running in a docker container inside an Ubuntu VM due to Windows Home not having Hyper-V; Now on Azure)</li>
</ul>
<br />
<ul>
  More info:
  <li>Running on Azure App Service (not anymore, since my credits depleted)</li>
  <li>User and system dynamically uploaded files are stored in an Azure private container, and served with a 5 seconds expiring SAS</li>
  <li>Azure storage integration using django-storages</li>
  <li>Static files are served by WhiteNoise</li>
  <li>Account registration with e-mail confirmation and 1 more step validation (by specific user group)</li>
  <li>Ajax requests to make the app dynamic</li>
</ul>
<br />
<ul>
  <h3>@TODO</h3>
  <li>Retrieve chat log</li>
  <li>Ticket status flow</li>
</ul>
