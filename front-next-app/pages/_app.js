import { AuthProvider } from '../contexts/AuthContext';
import { ApolloProvider } from '@apollo/client';
import { useApollo } from '../lib/apolloClient';
import '../styles/global.css';

function MyApp({ Component, pageProps }) {
    const apolloClient = useApollo(pageProps.initialApolloState);

    return (
        <ApolloProvider client={apolloClient}>
            <AuthProvider>
                <Component {...pageProps} />
            </AuthProvider>
        </ApolloProvider>

    );
}

export default MyApp;
