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
    let safetyCounter = 0
    const MAX_PAGES = 100 // Safety limit

    while(safetyCounter < MAX_PAGES){
      const r:any = await this.client.request(q, { login, after })
      const page = r.user.repositories
      nodes.push(...page.nodes)
      
      if(!page.pageInfo.hasNextPage) break
      
      // FIX: Prevent infinite loop if cursor doesn't change
      if(after === page.pageInfo.endCursor) break
      
      after = page.pageInfo.endCursor
      safetyCounter++
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
