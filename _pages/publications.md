---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---

{% if site.author.googlescholar %}
  <div class="wordwrap">(Work in Progress) All of my work that I have made some significant research contribution towards and has been published in some venue are listed here. You can find a comprehensive list of my work on <a href="{{https://scholar.google.com/citations?user=uGTn8fUAAAAJ&hl=en}}">my Google Scholar profile</a>. </div>
{% endif %}

{% include base_path %}

{% for post in site.publications reversed %}
  {% include archive-single.html %}
{% endfor %}
