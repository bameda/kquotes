import graphene
from graphene import AbstractType

from graphene_django.filter import DjangoFilterConnectionField

from kquotes.auth.decorators import login_required

from .models import Quote
from .nodes import QuoteNode


class QuotesQuery(AbstractType):
    quote = graphene.Field(QuoteNode)
    quotes = DjangoFilterConnectionField(QuoteNode)

    @login_required
    def resolve_quote(self, args, context, info):
        return Quote.objects.all()

    @login_required
    def resolve_quotes(self, args, context, info):
        """
        Operation:
            query quotes ($first: Int){
              quotes(last: $first){
                pageInfo {
                  hasNextPage
                  hasPreviousPage
                  startCursor
                  endCursor
                }
                edges {
                  node {
                    id
                    quote
                    explanation
                    author {
                      username
                      firstName
                      lastName
                    }
                    externalAuthor
                    creator {
                      username
                      firstName
                      lastName
                    }
                    createdDate
                    scores {
                      score
                      createdDate
                      user {
                        username
                        firstName
                        lastName
                      }
                    }
                  }
                }
              }
            }

            Vars:
                {
                    "first": 10
                }
        """
        return Quote.objects.all()
