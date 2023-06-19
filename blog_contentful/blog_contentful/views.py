import os

import contentful
import markdown
from django.http import Http404
from django.shortcuts import render
from dotenv import load_dotenv

load_dotenv()

client = contentful.Client(
    os.environ.get('CTF_SPACE_ID'),
    os.environ.get('CTF_DELIVERY_KEY'),
)

def posts(request):
    return render(request, 'posts.html', {
        'posts': client.entries(
            {'content_type': 'blogPost'}
        )
    })

def post_by_slug(request, slug):
    try:
        post = client.entries(
            {'content_type': 'blogPost', 'fields.slug': slug}
        )[0]
        html = markdown.markdown(post.content)
        return render(request, 'post_by_slug.html', {'post': post, 'html': html})
    except IndexError:
        raise Http404('Post not found for slug: {0}'.format(slug))
