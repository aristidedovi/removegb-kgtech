import { useContext, useEffect } from 'react';
import { useRouter } from 'next/router';
import AuthContext from '../contexts/AuthContext';
import dynamic from 'next/dynamic' 
import { gql, useQuery } from '@apollo/client';
import { initializeApollo } from '../lib/apolloClient';

const ALL_USERS_QUERY = gql`
  query AllUsers {
    users {
      id
      username
      role
    }
  }
`;

const Dashboard = () => {
  const { loading, error, data } = useQuery(ALL_USERS_QUERY);
  const { isAuthenticated, authToken } = useContext(AuthContext);
  const router = useRouter();


  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');  // Redirect to login page if not authenticated
    }
  }, [isAuthenticated, router]);

   // Handle the loading state
   if (loading) return <p>Loading...</p>;

   // Handle errors from the query
   if (error) return <p>Error: {error.message}</p>;

  if (!isAuthenticated) {
    return <p>Redirecting to login...</p>;
  }

  // Handle the case when data is undefined or the users array is empty
  if (!data || !data.users || data.users.length === 0) {
    return <p>No users found</p>;
  }
  

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Welcome to the dashboard!</p>
      <ul>
        {data.users.map((user) => (
          <li key={user.id}>
            {user.username} ({user.role})
          </li>
        ))}
      </ul>
    </div>
  );
};

// If you want to use SSR or SSG, you can do it like this:
// export async function getStaticProps() {
//   const apolloClient = initializeApollo();

//   await apolloClient.query({
//     query: ALL_USERS_QUERY,
//   });

//   return {
//     props: {
//       initialApolloState: apolloClient.cache.extract(),
//     },
//   };
// }

//export default Dashboard;
export default dynamic(() => Promise.resolve(Dashboard), { ssr: false });

