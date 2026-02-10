import { GraphQLClient, gql } from 'graphql-request'
import Bottleneck from 'bottleneck'
import fetch from 'node-fetch'
import { config } from './config'
import { logger } from './logger'

export class GitHub {
  client: GraphQLClient
  limiter: Bottleneck
  constructor(token: string){
    this.client = new GraphQLClient(config.githubApi, { headers: { Authorization: `Bearer ${token}` }})
    this.limiter = new Bottleneck({ minTime: 200 })
  }
  async viewer(){
    return this.client.request(gql`{ viewer { login } }`)
  }
  async reposByUser(login: string){
    const q = gql`
      query($login:String!, $after:String){
        user(login:$login){
          repositories(first:100, after:$after, orderBy:{field:UPDATED_AT, direction:DESC}){
            pageInfo{ hasNextPage endCursor }
            nodes{ name description isPrivate stargazerCount forkCount updatedAt pushedAt defaultBranchRef{ name } }
          }
        }
      }`
    let after: string|undefined
    const nodes:any[]=[]
    while(true){
      const r:any = await this.client.request(q, { login, after })
      const page = r.user.repositories
      nodes.push(...page.nodes)
      if(!page.pageInfo.hasNextPage) break
      after = page.pageInfo.endCursor
    }
    return nodes
  }
  async createIssue(owner:string, repo:string, title:string, body:string){
    const q = gql`
      mutation($repoId:ID!, $title:String!, $body:String){
        createIssue(input:{repositoryId:$repoId, title:$title, body:$body}){ issue{ number url } }
      }`
    const repoQ = gql`query($owner:String!, $name:String!){ repository(owner:$owner, name:$name){ id } }`
    const repoMeta:any = await this.client.request(repoQ, { owner, name: repo })
    return this.client.request(q, { repoId: repoMeta.repository.id, title, body })
  }
}
