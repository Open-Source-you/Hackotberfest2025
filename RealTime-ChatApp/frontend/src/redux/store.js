import { configureStore } from '@reduxjs/toolkit';
import { persistStore, persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage'; // defaults to localStorage for web
import userReducer from './userSlice';
import messageReducer from './messageSlice';
import socketReducer from './socketSlice';

// Persist configuration
const persistConfig = {
  key: 'root', // key for storing the state in storage
  storage,     // the storage engine
};

// Combine the reducers
const rootReducer = {
  user: persistReducer(persistConfig, userReducer),
  message: messageReducer,  // Not persisting this one as an example
  socket: socketReducer     // Not persisting this one as an example
};

// Configure the store
const store = configureStore({
  reducer: rootReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false, // Disable serializable check due to redux-persist
    }),
});

// Create a persistor
export const persistor = persistStore(store);

export default store;
